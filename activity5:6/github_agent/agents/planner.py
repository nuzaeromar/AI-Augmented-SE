"""
agents/planner.py
Planner Agent — decides what action to take and how to frame it.
Pattern: Planning — structured decision before any drafting begins.
"""
from typing import Optional, Callable
from agents.base import BaseAgent
from models.schemas import ReviewResult, DiffContext, PlanResult
from config import Config


class PlannerAgent(BaseAgent):
    """
    Takes review output + optional user instruction.
    Produces a structured plan: action, scope, hints for Writer.
    """

    def __init__(self, cfg: Config):
        super().__init__(cfg, "Planner")

    def run(
        self,
        review: ReviewResult,
        diff_ctx: DiffContext,
        instruction: str = "",
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> PlanResult:
        _emit(emit, self.name, "Building action plan…")

        instruction_block = ""
        if instruction:
            instruction_block = f"\nUSER INSTRUCTION:\n{instruction}\n"

        issues_block = "\n".join(f"- {i}" for i in review.issues_found) or "- None"

        prompt = f"""You are a technical project manager planning the next step after a code review.

REVIEW SUMMARY:
{review.summary}

ISSUES FOUND:
{issues_block}

RECOMMENDED ACTION: {review.recommended_action}
RISK LEVEL: {review.risk}
CATEGORY: {review.category}
JUSTIFICATION: {review.justification}
{instruction_block}

Your job:
1. Validate the scope of action.
2. Decide the final action: create_issue | create_pr | no_action
3. Provide clear hints for the Writer agent.

Respond ONLY with valid JSON:
{{
  "action": "create_issue|create_pr|no_action",
  "scope": "brief description of exactly what will be created",
  "rationale": "why this action is correct given the evidence",
  "draft_hints": [
    "hint 1 for the Writer about what to include",
    "hint 2",
    "hint 3"
  ],
  "risks": ["risk 1", "risk 2"]
}}"""

        _emit(emit, self.name, "Calling LLM for planning…")
        raw  = self.chat([{"role": "user", "content": prompt}])
        data = self.parse_json(raw)

        if not data:
            _emit(emit, self.name, "Warning: could not parse plan — using defaults")
            data = {
                "action":      review.recommended_action,
                "scope":       "Auto-determined from review",
                "rationale":   review.justification,
                "draft_hints": ["Follow review findings", "Include evidence"],
                "risks":       review.issues_found[:2],
            }

        result = PlanResult.from_dict(data)
        _emit(emit, self.name,
              f"Plan validated — action: {result.action} | scope: {result.scope}")
        return result


def _emit(fn, agent: str, msg: str) -> None:
    if fn:
        fn(agent, msg)
