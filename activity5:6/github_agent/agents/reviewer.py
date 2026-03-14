"""
agents/reviewer.py
Reviewer Agent — analyzes git diff and code.
Pattern: Tool Use (Python reads files/diff) + Planning start.
"""
from typing import Optional, Callable
from agents.base import BaseAgent
from models.schemas import DiffContext, ReviewResult
from config import Config


class ReviewerAgent(BaseAgent):
    """
    Receives a DiffContext (already gathered by Python tools),
    sends it to the LLM for analysis, returns a ReviewResult.
    """

    def __init__(self, cfg: Config):
        super().__init__(cfg, "Reviewer")

    def run(
        self,
        diff_ctx: DiffContext,
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> ReviewResult:
        _emit(emit, self.name, f"Analyzing diff — {len(diff_ctx.files_changed)} file(s) changed")
        _emit(emit, self.name, f"[tool] diff stats: +{diff_ctx.insertions} -{diff_ctx.deletions} lines")

        diff_preview = diff_ctx.diff_text[:self.cfg.MAX_DIFF_CHARS]
        if len(diff_ctx.diff_text) > self.cfg.MAX_DIFF_CHARS:
            diff_preview += "\n... [diff truncated]"

        files_list = "\n".join(f"  - {f}" for f in diff_ctx.files_changed) or "  (none detected)"

        prompt = f"""You are a senior software engineer doing a code review.

Analyze the following git diff carefully.

COMMIT RANGE: {diff_ctx.commit_range}
BRANCH: {diff_ctx.branch}
FILES CHANGED:
{files_list}
INSERTIONS: {diff_ctx.insertions}
DELETIONS: {diff_ctx.deletions}

GIT DIFF:
{diff_preview}

Respond ONLY with a valid JSON object — no markdown, no explanation:
{{
  "summary": "one-paragraph summary of what changed",
  "issues_found": ["issue 1", "issue 2"],
  "category": "feature|bugfix|refactor|docs|test|config|unknown",
  "risk": "low|medium|high",
  "recommended_action": "create_issue|create_pr|no_action",
  "justification": "why you recommend this action with evidence from the diff",
  "files_reviewed": ["file1.py", "file2.js"]
}}"""

        _emit(emit, self.name, "Calling LLM for code analysis…")
        raw = self.chat([{"role": "user", "content": prompt}])
        data = self.parse_json(raw)

        if not data:
            _emit(emit, self.name, "Warning: LLM returned unparseable JSON — using fallback")
            data = {
                "summary": raw[:300],
                "issues_found": ["Could not parse structured analysis"],
                "category": "unknown",
                "risk": "medium",
                "recommended_action": "no_action",
                "justification": "Parse error — manual review recommended",
                "files_reviewed": diff_ctx.files_changed,
            }

        result = ReviewResult.from_dict(data)
        result.files_reviewed = result.files_reviewed or diff_ctx.files_changed

        _emit(emit, self.name,
              f"Review complete — category: {result.category} | risk: {result.risk} | "
              f"action: {result.recommended_action}")
        return result


def _emit(fn, agent: str, msg: str) -> None:
    if fn:
        fn(agent, msg)
