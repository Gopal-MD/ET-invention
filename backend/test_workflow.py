from workflow import run_assessment_workflow


def test_workflow_exposes_real_stage_states_and_review_pause():
    state = run_assessment_workflow("ASMT-1", "Quarterly reporting", "Retail Banking")
    assert state.review_required is True
    assert state.result["gap"] == "GAP-1042"
    assert any(event["status"] == "Needs Review" for event in state.stage_events)
    assert "Risk scoring" in state.completed_stages