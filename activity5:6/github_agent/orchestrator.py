"""
orchestrator.py
Manages the multi-agent pipeline.

Pipelines:
  review   → Reviewer → Planner → (optional Writer + Gatekeeper)
  draft    → (optional Reviewer) → Planner → Writer → Gatekeeper
  improve  → Writer.improve → Gatekeeper.reflect
"""
import json
from pathlib import Path
from typing import Optional, Callable

from config import Config
from models.schemas import (
    AgentReport, DiffContext, ReviewResult,
    IssueDraft, PRDraft, ImprovementResult,
)
from agents.reviewer   import ReviewerAgent
from agents.planner    import PlannerAgent
from agents.writer     import WriterAgent
from agents.gatekeeper import GatekeeperAgent
from tools.git_tools   import (
    get_diff, get_diff_range, get_changed_files,
    get_diff_stat, get_current_branch, is_git_repo,
)
from tools.github_tools import GitHubClient


class Orchestrator:

    def __init__(self, cfg: Config):
        self.cfg        = cfg
        self.reviewer   = ReviewerAgent(cfg)
        self.planner    = PlannerAgent(cfg)
        self.writer     = WriterAgent(cfg)
        self.gatekeeper = GatekeeperAgent(cfg)
        self.github     = GitHubClient(cfg)

    # ── Pipeline 1: Review Changes ────────────────────────────────────────────

    def review(
        self,
        base:         str = "main",
        commit_range: str = "",
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> AgentReport:
        _emit(emit, "Orchestrator", "Starting review pipeline…")

        diff_ctx = self._gather_diff(base, commit_range, emit)

        review = self.reviewer.run(diff_ctx, emit)
        plan   = self.planner.run(review, diff_ctx, emit=emit)

        report        = AgentReport(task="review")
        report.review = review
        report.plan   = plan

        _emit(emit, "Orchestrator",
              f"Review complete — recommended action: {plan.action}")
        _save_state(self.cfg, report)
        return report

    # ── Pipeline 2: Draft Issue or PR ─────────────────────────────────────────

    def draft(
        self,
        kind:        str,   # "issue" | "pr"
        instruction: str = "",
        base:        str = "main",
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> AgentReport:
        _emit(emit, "Orchestrator", f"Starting draft-{kind} pipeline…")

        diff_ctx = self._gather_diff(base, "", emit)
        review   = self.reviewer.run(diff_ctx, emit)
        plan     = self.planner.run(review, diff_ctx, instruction, emit)

        report        = AgentReport(task=f"draft_{kind}")
        report.review = review
        report.plan   = plan

        if kind == "issue":
            draft = self.writer.draft_issue(plan, review, diff_ctx, instruction, emit)
            report.draft_issue  = draft
            report.reflection   = self.gatekeeper.reflect_issue(draft, emit)
        else:
            draft = self.writer.draft_pr(plan, review, diff_ctx, instruction, emit)
            report.draft_pr   = draft
            report.reflection = self.gatekeeper.reflect_pr(draft, emit)

        verdict = report.reflection.verdict
        _emit(emit, "Gatekeeper",
              f"Reflection verdict: {verdict}" +
              (" — revision required" if verdict == "FAIL" else " — safe to proceed"))

        _save_state(self.cfg, report)
        return report

    # ── Pipeline 3: Approve and Create ────────────────────────────────────────

    def approve(
        self,
        approved: bool,
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> AgentReport:
        report = _load_state(self.cfg)
        if not report:
            raise RuntimeError(
                "No pending draft found. Run `agent draft` first."
            )

        report.approved = approved

        if not approved:
            _emit(emit, "Gatekeeper", "Draft rejected. No changes made.")
            _save_state(self.cfg, report)
            return report

        # Check reflection passed
        if report.reflection and not report.reflection.safe_to_proceed:
            _emit(emit, "Gatekeeper",
                  "Cannot approve — reflection verdict is FAIL. Revise first.")
            report.approved = False
            return report

        _emit(emit, "Gatekeeper", "Approval received — creating on GitHub…")

        try:
            if report.draft_issue:
                d = report.draft_issue
                _emit(emit, "Gatekeeper", "[tool] GitHub API: create issue")
                result    = self.github.create_issue(
                    d.title, d.to_markdown(), d.labels
                )
                report.github_url = result.get("html_url", "")
                _emit(emit, "Gatekeeper", f"Issue created: {report.github_url}")

            elif report.draft_pr:
                d    = report.draft_pr
                branch = get_current_branch(self.cfg.REPO_PATH)
                _emit(emit, "Gatekeeper", "[tool] GitHub API: create pull request")
                result    = self.github.create_pr(
                    d.title, d.to_markdown(), head=branch,
                    base=d.base_branch, labels=d.labels
                )
                report.github_url = result.get("html_url", "")
                _emit(emit, "Gatekeeper", f"PR created: {report.github_url}")

            elif report.improvement:
                imp = report.improvement
                _emit(emit, "Gatekeeper",
                      f"[tool] GitHub API: update {imp.kind} #{imp.original_number}")
                if imp.kind == "issue":
                    result = self.github.update_issue(
                        imp.original_number, imp.improved_title, imp.improved_body
                    )
                else:
                    result = self.github.update_pr(
                        imp.original_number, imp.improved_title, imp.improved_body
                    )
                report.github_url = result.get("html_url", "")
                _emit(emit, "Gatekeeper", f"Updated: {report.github_url}")

        except Exception as e:
            report.error = str(e)
            _emit(emit, "Gatekeeper", f"GitHub API error: {e}")

        _save_state(self.cfg, report)
        return report

    # ── Pipeline 4: Improve Existing Issue/PR ─────────────────────────────────

    def improve(
        self,
        kind:   str,
        number: int,
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> AgentReport:
        _emit(emit, "Orchestrator", f"Starting improve-{kind} pipeline for #{number}…")

        if not self.github.is_configured():
            raise RuntimeError(
                "GitHub not configured. Set GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO."
            )

        _emit(emit, "Reviewer", f"[tool] Fetching {kind} #{number} from GitHub…")
        try:
            if kind == "issue":
                data = self.github.get_issue(number)
            else:
                data = self.github.get_pr(number)
        except Exception as e:
            raise RuntimeError(f"Could not fetch {kind} #{number}: {e}")

        original_title = data.get("title", "")
        original_body  = data.get("body", "") or ""

        _emit(emit, "Reviewer",
              f"Fetched: \"{original_title}\" ({len(original_body)} chars)")

        improvement = self.writer.improve(number, kind, original_title, original_body, emit)
        reflection  = self.gatekeeper.reflect_improvement(improvement, emit)
        improvement.reflection = reflection

        report             = AgentReport(task=f"improve_{kind}")
        report.improvement = improvement
        report.reflection  = reflection

        _save_state(self.cfg, report)
        return report

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _gather_diff(
        self,
        base:         str,
        commit_range: str,
        emit: Optional[Callable[[str, str], None]],
    ) -> DiffContext:
        repo = self.cfg.REPO_PATH

        if not is_git_repo(repo):
            _emit(emit, "Orchestrator",
                  f"Warning: {repo} is not a git repo — using empty diff")
            return DiffContext(
                diff_text="",
                files_changed=[],
                insertions=0,
                deletions=0,
                commit_range=commit_range or f"HEAD vs {base}",
                branch="unknown",
            )

        branch = get_current_branch(repo)
        _emit(emit, "Orchestrator", f"[tool] git branch: {branch}")

        if commit_range:
            _emit(emit, "Orchestrator", f"[tool] git diff {commit_range}")
            diff_text     = get_diff_range(repo, commit_range)
            files_changed = [f for f in diff_text.splitlines()
                             if f.startswith("diff --git")]
            # parse filenames from diff header
            import re
            files_changed = re.findall(r"diff --git a/(.*?) b/", diff_text)
            label = commit_range
        else:
            _emit(emit, "Orchestrator", f"[tool] git diff {base}...HEAD")
            diff_text     = get_diff(repo, base)
            files_changed = get_changed_files(repo, base)
            label         = f"HEAD vs {base}"

        insertions, deletions = get_diff_stat(repo, base)
        _emit(emit, "Orchestrator",
              f"[tool] {len(files_changed)} file(s) changed, "
              f"+{insertions} -{deletions} lines")

        return DiffContext(
            diff_text     = diff_text,
            files_changed = files_changed,
            insertions    = insertions,
            deletions     = deletions,
            commit_range  = label,
            branch        = branch,
        )


# ── State persistence ─────────────────────────────────────────────────────────

def _save_state(cfg: Config, report: AgentReport) -> None:
    try:
        Path(cfg.STATE_FILE).write_text(
            json.dumps(report.to_dict(), indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


def _load_state(cfg: Config) -> Optional[AgentReport]:
    try:
        path = Path(cfg.STATE_FILE)
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        report = AgentReport(task=data.get("task", ""))
        report.approved   = data.get("approved")
        report.github_url = data.get("github_url", "")
        report.error      = data.get("error", "")

        from models.schemas import (
            ReviewResult, PlanResult, IssueDraft,
            PRDraft, ReflectionResult, ImprovementResult,
        )
        if "review"      in data: report.review      = ReviewResult.from_dict(data["review"])
        if "plan"        in data: report.plan        = PlanResult.from_dict(data["plan"])
        if "draft_issue" in data: report.draft_issue = IssueDraft.from_dict(data["draft_issue"])
        if "draft_pr"    in data: report.draft_pr    = PRDraft.from_dict(data["draft_pr"])
        if "reflection"  in data: report.reflection  = ReflectionResult.from_dict(data["reflection"])
        if "improvement" in data:
            imp_data = data["improvement"]
            refl = None
            if "reflection" in imp_data:
                refl = ReflectionResult.from_dict(imp_data["reflection"])
            report.improvement = ImprovementResult(
                original_number = imp_data.get("original_number", 0),
                kind            = imp_data.get("kind", "issue"),
                critique        = imp_data.get("critique", []),
                improved_title  = imp_data.get("improved_title", ""),
                improved_body   = imp_data.get("improved_body", ""),
                changes_made    = imp_data.get("changes_made", []),
                reflection      = refl,
            )
        return report
    except Exception:
        return None


def _emit(fn, agent: str, msg: str) -> None:
    if fn:
        fn(agent, msg)
