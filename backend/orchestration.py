import json
from pathlib import Path
from typing import Any

from workflow import run_assessment_workflow


class WorkflowCheckpointStore:
    def __init__(self, checkpoint_dir: str | Path | None = None):
        self.checkpoint_dir = Path(checkpoint_dir or Path(__file__).resolve().parent / ".checkpoints")
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, assessment_id: str) -> Path:
        return self.checkpoint_dir / f"{assessment_id}.json"

    def create(self, assessment_id: str, scope: str, business_unit: str) -> dict[str, Any]:
        state = run_assessment_workflow(assessment_id, scope, business_unit)
        payload = {
            "assessment_id": assessment_id,
            "status": "completed" if state.result else "ready",
            "mode": "deterministic-fallback",
            "review_required": state.review_required,
            "state": {
                "assessment_id": state.assessment_id,
                "scope": state.scope,
                "business_unit": state.business_unit,
                "current_stage": state.current_stage,
                "completed_stages": state.completed_stages,
                "stage_events": state.stage_events,
                "review_required": state.review_required,
                "result": state.result,
            },
            "last_updated": state.stage_events[-1]["stage"] if state.stage_events else "Input validation",
        }
        self._path(assessment_id).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return payload

    def load(self, assessment_id: str) -> dict[str, Any]:
        path = self._path(assessment_id)
        if not path.exists():
            return {"assessment_id": assessment_id, "status": "missing", "state": {"review_required": False}}
        return json.loads(path.read_text(encoding="utf-8"))


def run_durable_workflow(assessment_id: str, scope: str, business_unit: str, checkpoint_store: WorkflowCheckpointStore | None = None) -> dict[str, Any]:
    store = checkpoint_store or WorkflowCheckpointStore()
    return store.create(assessment_id, scope, business_unit)
