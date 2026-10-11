from dataclasses import dataclass, field
from typing import Any, Literal

StageStatus = Literal["Pending", "Running", "Completed", "Needs Review", "Failed", "Skipped"]


@dataclass
class AssessmentState:
    assessment_id: str
    scope: str
    business_unit: str
    current_stage: str = "Input validation"
    completed_stages: list[str] = field(default_factory=list)
    stage_events: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    review_required: bool = False
    result: dict[str, Any] = field(default_factory=dict)


def _complete(state: AssessmentState, stage: str, output: dict[str, Any] | None = None, status: StageStatus = "Completed") -> None:
    state.current_stage = stage
    state.stage_events.append({"stage": stage, "status": status, "output": output or {}})
    if status == "Completed":
        state.completed_stages.append(stage)


def run_assessment_workflow(assessment_id: str, scope: str, business_unit: str) -> AssessmentState:
    state = AssessmentState(assessment_id=assessment_id, scope=scope, business_unit=business_unit)
    _complete(state, "Input validation", {"scope_valid": True})
    _complete(state, "Regulatory retrieval", {"source": "DOC-001", "mode": "lexical-demo"})
    _complete(state, "Obligation extraction", {"obligation": "OBL-007", "citation": "§9.1"})
    _complete(state, "Applicability analysis", {"status": "Applicable", "profile": "synthetic-bank-demo"})
    _complete(state, "Control mapping", {"control": "CTL-003", "mapping": "partial"}, "Needs Review")
    state.review_required = True
    _complete(state, "Evidence review", {"evidence": "EVD-001", "status": "incomplete"}, "Needs Review")
    _complete(state, "Deterministic compliance checks", {"test_result": "gap_identified"})
    _complete(state, "Gap identification", {"gap": "GAP-1042"})
    _complete(state, "Risk scoring", {"score": 96, "severity": "Critical"})
    _complete(state, "Remediation recommendation", {"approval_required": True})
    _complete(state, "Audit record creation", {"audit_required": True})
    state.result = {"obligation": "OBL-007", "control": "CTL-003", "evidence": "EVD-001", "gap": "GAP-1042", "risk_score": 96, "severity": "Critical"}
    return state
