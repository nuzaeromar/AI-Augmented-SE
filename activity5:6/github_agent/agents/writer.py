"""
agents/writer.py
Writer Agent — drafts Issues, PRs, and improvement suggestions.
Pattern: Tool Use (reads existing issues/PRs), Multi-agent output.
"""
from typing import Optional, Callable
from agents.base import BaseAgent
from models.schemas import (
    PlanResult, ReviewResult, DiffContext,
    IssueDraft, PRDraft, ImprovementResult,
)
from config import Config


class WriterAgent(BaseAgent):
    """Drafts structured GitHub Issues and Pull Requests."""

    def __init__(self, cfg: Config):
        super().__init__(cfg, "Writer")

    # ── Draft Issue ───────────────────────────────────────────────────────────

    def draft_issue(
        self,
        plan: PlanResult,
        review: ReviewResult,
        diff_ctx: DiffContext,
        instruction: str = "",
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> IssueDraft:
        _emit(emit, self.name, "Drafting GitHub Issue…")

        hints_block  = "\n".join(f"- {h}" for h in plan.draft_hints)
        issues_block = "\n".join(f"- {i}" for i in review.issues_found)
        files_block  = "\n".join(f"- {f}" for f in diff_ctx.files_changed)
        instruction_block = f"\nUSER INSTRUCTION:\n{instruction}\n" if instruction else ""

        prompt = f"""You are a technical writer creating a GitHub Issue.

PLAN:
Action: {plan.action}
Scope: {plan.scope}
Rationale: {plan.rationale}
{instruction_block}
REVIEW FINDINGS:
Summary: {review.summary}
Issues:
{issues_block}
Risk: {review.risk}
Category: {review.category}

FILES CHANGED:
{files_block}

WRITER HINTS:
{hints_block}

Write a clear, professional GitHub Issue. Respond ONLY with valid JSON:
{{
  "title": "concise issue title (max 80 chars)",
  "problem_description": "2-3 paragraph description of the problem with context",
  "evidence": [
    "specific evidence item 1 from the diff or code",
    "specific evidence item 2",
    "specific evidence item 3"
  ],
  "acceptance_criteria": [
    "criterion 1 — measurable, testable",
    "criterion 2",
    "criterion 3"
  ],
  "risk_level": "low|medium|high",
  "labels": ["bug", "enhancement", "documentation", etc — pick appropriate ones]
}}"""

        _emit(emit, self.name, "Calling LLM for issue draft…")
        raw  = self.chat([{"role": "user", "content": prompt}], temperature=0.4)
        data = self.parse_json(raw)

        if not data or not data.get("title"):
            _emit(emit, self.name, "Warning: using fallback issue structure")
            data = {
                "title":               f"[{review.category.upper()}] {review.summary[:60]}",
                "problem_description": review.summary,
                "evidence":            review.issues_found[:3],
                "acceptance_criteria": ["Issue is resolved and tests pass"],
                "risk_level":          review.risk,
                "labels":              [review.category],
            }

        draft = IssueDraft.from_dict(data)
        _emit(emit, self.name, f"Issue draft ready: \"{draft.title}\"")
        return draft

    # ── Draft PR ──────────────────────────────────────────────────────────────

    def draft_pr(
        self,
        plan: PlanResult,
        review: ReviewResult,
        diff_ctx: DiffContext,
        instruction: str = "",
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> PRDraft:
        _emit(emit, self.name, "Drafting GitHub Pull Request…")

        hints_block  = "\n".join(f"- {h}" for h in plan.draft_hints)
        files_block  = "\n".join(f"- {f}" for f in diff_ctx.files_changed)
        instruction_block = f"\nUSER INSTRUCTION:\n{instruction}\n" if instruction else ""

        diff_preview = diff_ctx.diff_text[:3000]

        prompt = f"""You are a senior engineer writing a GitHub Pull Request description.

PLAN:
Scope: {plan.scope}
Rationale: {plan.rationale}
{instruction_block}
REVIEW:
Summary: {review.summary}
Category: {review.category}
Risk: {review.risk}
Branch: {diff_ctx.branch}

FILES CHANGED:
{files_block}

DIFF PREVIEW:
{diff_preview}

WRITER HINTS:
{hints_block}

Write a clear, professional PR description. Respond ONLY with valid JSON:
{{
  "title": "PR title (max 80 chars, use imperative: Add/Fix/Refactor/Update)",
  "summary": "2-3 paragraph summary of what this PR does and why",
  "files_affected": ["file1.py", "file2.js"],
  "behavior_change": "what behavior changes for end users or developers",
  "test_plan": "specific steps to test this change",
  "risk_level": "low|medium|high",
  "base_branch": "main",
  "labels": ["enhancement", "bug", "refactor" — pick appropriate]
}}"""

        _emit(emit, self.name, "Calling LLM for PR draft…")
        raw  = self.chat([{"role": "user", "content": prompt}], temperature=0.4)
        data = self.parse_json(raw)

        if not data or not data.get("title"):
            _emit(emit, self.name, "Warning: using fallback PR structure")
            data = {
                "title":           f"[{review.category.upper()}] {review.summary[:60]}",
                "summary":         review.summary,
                "files_affected":  diff_ctx.files_changed,
                "behavior_change": "See diff for details",
                "test_plan":       "Run existing test suite",
                "risk_level":      review.risk,
                "base_branch":     "main",
                "labels":          [review.category],
            }

        data["files_affected"] = data.get("files_affected") or diff_ctx.files_changed
        draft = PRDraft.from_dict(data)
        _emit(emit, self.name, f"PR draft ready: \"{draft.title}\"")
        return draft

    # ── Improve existing Issue/PR ─────────────────────────────────────────────

    def improve(
        self,
        number: int,
        kind: str,         # "issue" | "pr"
        original_title: str,
        original_body:  str,
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> ImprovementResult:
        _emit(emit, self.name, f"Analyzing existing {kind} #{number}…")

        prompt = f"""You are a senior engineer improving an existing GitHub {kind.upper()}.

ORIGINAL TITLE: {original_title}

ORIGINAL BODY:
{original_body[:4000]}

Step 1 — CRITIQUE (be specific):
Identify what is unclear, missing, or vague.

Step 2 — IMPROVE:
Write a complete improved version.

Respond ONLY with valid JSON:
{{
  "critique": [
    "specific problem 1",
    "specific problem 2",
    "specific problem 3"
  ],
  "improved_title": "better, clearer title",
  "improved_body": "complete improved body in markdown — include all sections",
  "changes_made": [
    "change 1 description",
    "change 2 description"
  ]
}}"""

        _emit(emit, self.name, f"Calling LLM to critique and rewrite {kind}…")
        raw  = self.chat([{"role": "user", "content": prompt}], temperature=0.4)
        data = self.parse_json(raw)

        result = ImprovementResult(
            original_number = number,
            kind            = kind,
            critique        = data.get("critique", ["Could not generate critique"]),
            improved_title  = data.get("improved_title", original_title),
            improved_body   = data.get("improved_body", original_body),
            changes_made    = data.get("changes_made", []),
        )

        _emit(emit, self.name,
              f"Improvement ready — {len(result.critique)} critique points, "
              f"{len(result.changes_made)} changes")
        return result


def _emit(fn, agent: str, msg: str) -> None:
    if fn:
        fn(agent, msg)
