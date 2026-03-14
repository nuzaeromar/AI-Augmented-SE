"""
models/schemas.py
Typed dataclasses for all pipeline outputs.
Passed between agents — no raw dicts crossing boundaries.
"""
from dataclasses import dataclass, field
from typing import List, Optional


# ── Diff / Code Analysis ──────────────────────────────────────────────────────

@dataclass
class DiffContext:
    """Raw diff data gathered by Python tools before LLM sees it."""
    diff_text:     str
    files_changed: List[str]
    insertions:    int
    deletions:     int
    commit_range:  str
    branch:        str = "current"

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class ReviewResult:
    """Output from the Reviewer agent."""
    summary:            str
    issues_found:       List[str]
    category:           str          # feature | bugfix | refactor | docs | test | config
    risk:               str          # low | medium | high
    recommended_action: str          # create_issue | create_pr | no_action
    justification:      str
    files_reviewed:     List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "ReviewResult":
        return cls(
            summary             = d.get("summary", ""),
            issues_found        = d.get("issues_found", []),
            category            = d.get("category", "unknown"),
            risk                = d.get("risk", "medium"),
            recommended_action  = d.get("recommended_action", "no_action"),
            justification       = d.get("justification", ""),
            files_reviewed      = d.get("files_reviewed", []),
        )


@dataclass
class PlanResult:
    """Output from the Planner agent."""
    action:      str
    scope:       str
    rationale:   str
    draft_hints: List[str]
    risks:       List[str]

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "PlanResult":
        return cls(
            action      = d.get("action", "no_action"),
            scope       = d.get("scope", ""),
            rationale   = d.get("rationale", ""),
            draft_hints = d.get("draft_hints", []),
            risks       = d.get("risks", []),
        )


@dataclass
class IssueDraft:
    """A drafted GitHub Issue."""
    title:               str
    problem_description: str
    evidence:            List[str]
    acceptance_criteria: List[str]
    risk_level:          str
    labels:              List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    def to_markdown(self) -> str:
        evidence_md = "\n".join(f"- {e}" for e in self.evidence)
        criteria_md = "\n".join(f"- [ ] {c}" for c in self.acceptance_criteria)
        labels_md   = ", ".join(f"`{l}`" for l in self.labels) or "None"
        return (
            f"## Problem Description\n{self.problem_description}\n\n"
            f"## Evidence\n{evidence_md}\n\n"
            f"## Acceptance Criteria\n{criteria_md}\n\n"
            f"**Risk Level:** `{self.risk_level}`  \n"
            f"**Labels:** {labels_md}"
        )

    @classmethod
    def from_dict(cls, d: dict) -> "IssueDraft":
        return cls(
            title               = d.get("title", ""),
            problem_description = d.get("problem_description", ""),
            evidence            = d.get("evidence", []),
            acceptance_criteria = d.get("acceptance_criteria", []),
            risk_level          = d.get("risk_level", "medium"),
            labels              = d.get("labels", []),
        )


@dataclass
class PRDraft:
    """A drafted GitHub Pull Request."""
    title:           str
    summary:         str
    files_affected:  List[str]
    behavior_change: str
    test_plan:       str
    risk_level:      str
    base_branch:     str = "main"
    labels:          List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    def to_markdown(self) -> str:
        files_md  = "\n".join(f"- `{f}`" for f in self.files_affected)
        labels_md = ", ".join(f"`{l}`" for l in self.labels) or "None"
        return (
            f"## Summary\n{self.summary}\n\n"
            f"## Files Affected\n{files_md}\n\n"
            f"## Behavior Change\n{self.behavior_change}\n\n"
            f"## Test Plan\n{self.test_plan}\n\n"
            f"**Risk Level:** `{self.risk_level}`  \n"
            f"**Base Branch:** `{self.base_branch}`  \n"
            f"**Labels:** {labels_md}"
        )

    @classmethod
    def from_dict(cls, d: dict) -> "PRDraft":
        return cls(
            title           = d.get("title", ""),
            summary         = d.get("summary", ""),
            files_affected  = d.get("files_affected", []),
            behavior_change = d.get("behavior_change", ""),
            test_plan       = d.get("test_plan", ""),
            risk_level      = d.get("risk_level", "medium"),
            base_branch     = d.get("base_branch", "main"),
            labels          = d.get("labels", []),
        )


@dataclass
class ReflectionResult:
    """Output from the Gatekeeper reflection step."""
    verdict:            str          # PASS | FAIL
    issues:             List[str]
    suggestions:        List[str]
    unsupported_claims: List[str]
    missing_fields:     List[str]
    safe_to_proceed:    bool

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "ReflectionResult":
        return cls(
            verdict             = d.get("verdict", "FAIL"),
            issues              = d.get("issues", []),
            suggestions         = d.get("suggestions", []),
            unsupported_claims  = d.get("unsupported_claims", []),
            missing_fields      = d.get("missing_fields", []),
            safe_to_proceed     = d.get("safe_to_proceed", False),
        )


@dataclass
class ImprovementResult:
    """Output from improve issue/PR flow."""
    original_number: int
    kind:            str
    critique:        List[str]
    improved_title:  str
    improved_body:   str
    changes_made:    List[str]
    reflection:      Optional[ReflectionResult] = None

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        if self.reflection:
            d["reflection"] = self.reflection.to_dict()
        return d


@dataclass
class AgentReport:
    """Top-level output returned by the orchestrator."""
    task:        str
    review:      Optional[ReviewResult]     = None
    plan:        Optional[PlanResult]       = None
    draft_issue: Optional[IssueDraft]       = None
    draft_pr:    Optional[PRDraft]          = None
    reflection:  Optional[ReflectionResult] = None
    improvement: Optional[ImprovementResult] = None
    github_url:  str                        = ""
    approved:    Optional[bool]             = None
    error:       str                        = ""

    def to_dict(self) -> dict:
        d: dict = {
            "task": self.task,
            "github_url": self.github_url,
            "approved": self.approved,
            "error": self.error,
        }
        if self.review:      d["review"]      = self.review.to_dict()
        if self.plan:        d["plan"]        = self.plan.to_dict()
        if self.draft_issue: d["draft_issue"] = self.draft_issue.to_dict()
        if self.draft_pr:    d["draft_pr"]    = self.draft_pr.to_dict()
        if self.reflection:  d["reflection"]  = self.reflection.to_dict()
        if self.improvement: d["improvement"] = self.improvement.to_dict()
        return d
