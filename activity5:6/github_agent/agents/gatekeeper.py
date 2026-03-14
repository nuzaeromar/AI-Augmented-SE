"""
agents/gatekeeper.py
Gatekeeper Agent — Reflection pattern + human approval gate.
Nothing reaches GitHub without passing through here.
"""
from typing import Optional, Callable, Union
from agents.base import BaseAgent
from models.schemas import (
    IssueDraft, PRDraft, ImprovementResult, ReflectionResult,
)
from config import Config


class GatekeeperAgent(BaseAgent):
    """
    Two responsibilities:
    1. Reflection: critique the draft for missing/unsupported content
    2. Approval gate: require explicit human yes/no before any write
    """

    def __init__(self, cfg: Config):
        super().__init__(cfg, "Gatekeeper")

    # ── Reflection ────────────────────────────────────────────────────────────

    def reflect_issue(
        self,
        draft: IssueDraft,
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> ReflectionResult:
        _emit(emit, self.name, "Running reflection on Issue draft…")

        prompt = f"""You are a strict quality reviewer checking a GitHub Issue draft before it is published.

ISSUE TITLE: {draft.title}
PROBLEM DESCRIPTION: {draft.problem_description}
EVIDENCE: {draft.evidence}
ACCEPTANCE CRITERIA: {draft.acceptance_criteria}
RISK LEVEL: {draft.risk_level}

Check for these problems:
1. Unsupported claims (assertions without evidence)
2. Missing evidence (claims without supporting data)
3. Vague acceptance criteria (not measurable or testable)
4. Missing fields (empty or placeholder content)
5. Policy violations (offensive, confidential, out of scope)

Respond ONLY with valid JSON:
{{
  "verdict": "PASS|FAIL",
  "issues": ["problem 1", "problem 2"],
  "suggestions": ["fix suggestion 1", "fix suggestion 2"],
  "unsupported_claims": ["claim without evidence"],
  "missing_fields": ["field name that is missing or vague"],
  "safe_to_proceed": true|false
}}

PASS means the draft is good enough to create. FAIL means revision is required."""

        return self._run_reflection(prompt, emit)

    def reflect_pr(
        self,
        draft: PRDraft,
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> ReflectionResult:
        _emit(emit, self.name, "Running reflection on PR draft…")

        prompt = f"""You are a strict quality reviewer checking a GitHub Pull Request draft.

PR TITLE: {draft.title}
SUMMARY: {draft.summary}
FILES AFFECTED: {draft.files_affected}
BEHAVIOR CHANGE: {draft.behavior_change}
TEST PLAN: {draft.test_plan}
RISK LEVEL: {draft.risk_level}

Check for:
1. Missing test plan (vague or absent testing instructions)
2. Unsupported claims about behavior changes
3. Missing files in the affected list
4. Incomplete or placeholder content
5. High risk with no mitigation mentioned

Respond ONLY with valid JSON:
{{
  "verdict": "PASS|FAIL",
  "issues": ["problem 1"],
  "suggestions": ["fix suggestion 1"],
  "unsupported_claims": ["claim without evidence"],
  "missing_fields": ["field that is missing"],
  "safe_to_proceed": true|false
}}"""

        return self._run_reflection(prompt, emit)

    def reflect_improvement(
        self,
        result: ImprovementResult,
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> ReflectionResult:
        _emit(emit, self.name, f"Reflecting on {result.kind} improvement…")

        prompt = f"""Review this proposed improvement to a GitHub {result.kind.upper()}.

CRITIQUE POINTS: {result.critique}
IMPROVED TITLE: {result.improved_title}
IMPROVED BODY (first 1500 chars): {result.improved_body[:1500]}
CHANGES MADE: {result.changes_made}

Does the improved version actually address all critique points?
Is it better than the original?

Respond ONLY with valid JSON:
{{
  "verdict": "PASS|FAIL",
  "issues": ["remaining problem"],
  "suggestions": ["further fix"],
  "unsupported_claims": [],
  "missing_fields": [],
  "safe_to_proceed": true|false
}}"""

        return self._run_reflection(prompt, emit)

    def _run_reflection(
        self,
        prompt: str,
        emit: Optional[Callable[[str, str], None]],
    ) -> ReflectionResult:
        raw  = self.chat([{"role": "user", "content": prompt}], temperature=0.2)
        data = self.parse_json(raw)

        if not data:
            result = ReflectionResult(
                verdict             = "FAIL",
                issues              = ["Could not parse reflection response"],
                suggestions         = ["Manual review required"],
                unsupported_claims  = [],
                missing_fields      = [],
                safe_to_proceed     = False,
            )
        else:
            result = ReflectionResult.from_dict(data)

        verdict_label = f"[bold green]PASS[/]" if result.verdict == "PASS" else "[bold red]FAIL[/]"
        _emit(emit, self.name, f"Reflection verdict: {result.verdict}")
        if result.issues:
            for issue in result.issues:
                _emit(emit, self.name, f"  ✗ {issue}")
        return result

    # ── Human Approval Gate ───────────────────────────────────────────────────

    def request_approval(
        self,
        draft: Union[IssueDraft, PRDraft, ImprovementResult],
        reflection: ReflectionResult,
        emit: Optional[Callable[[str, str], None]] = None,
    ) -> bool:
        """
        Show the draft + reflection to the user and ask for approval.
        Returns True if approved, False if rejected.
        """
        if self.cfg.AUTO_APPROVE and reflection.safe_to_proceed:
            _emit(emit, self.name, "AUTO_APPROVE=True — proceeding automatically")
            return True

        _emit(emit, self.name, "Awaiting human approval…")
        return False   # Web/CLI layers handle the actual prompt


def _emit(fn, agent: str, msg: str) -> None:
    if fn:
        fn(agent, msg)
