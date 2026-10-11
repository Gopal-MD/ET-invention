from fastapi.testclient import TestClient
from main import app, risk_severity

client = TestClient(app)

def test_health():
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'

def test_risk_thresholds():
    assert risk_severity(125) == 'Critical'
    assert risk_severity(79) == 'High'
    assert risk_severity(49) == 'Medium'
    assert risk_severity(1) == 'Low'

def test_assessment_is_traceable():
    response = client.post('/api/v1/assessments', json={'scope':'Q2 regulatory reporting','business_unit':'Retail Banking'})
    result = response.json()['result']
    assert result['citation']
    assert result['evidence']
    assert result['human_review_required'] is True
    assessment_id = response.json()['id']
    assert client.get(f'/api/v1/assessments/{assessment_id}').json()['id'] == assessment_id
    assert client.get('/api/v1/assessments').json()['total'] >= 1

def test_configuration_exposes_safe_model_status():
    response = client.get('/api/v1/configuration')
    assert response.status_code == 200
    payload = response.json()
    assert payload['model'] == 'llama-3.1-8b-instant'
    assert 'api_key' not in payload

def test_upload_is_persisted_and_audited():
    response = client.post('/api/v1/documents/upload', files={'file': ('sample.txt', b'regulatory text', 'text/plain')})
    assert response.status_code == 200
    document = response.json()
    assert document['status'] == 'processed'
    assert any(item['id'] == document['id'] for item in client.get('/api/v1/documents').json()['items'])
    assert any(item['record_id'] == document['id'] for item in client.get('/api/v1/audit-events').json()['items'])
    detail = client.get(f"/api/v1/documents/{document['id']}").json()
    assert detail['chunks'][0]['source_location'] == 'text:1'
    assert 'regulatory text' in detail['text']

def test_remediation_approval_creates_audit_event():
    response = client.post('/api/v1/remediation/GAP-1042/approve')
    assert response.status_code == 200
    event_id = response.json()['audit_event']
    assert any(item['id'] == event_id for item in client.get('/api/v1/audit-events').json()['items'])

def test_assistant_is_explicit_when_live_ai_is_unconfigured():
    response = client.post('/api/v1/assistant', json={'question': 'What evidence is missing?'})
    assert response.status_code == 200
    assert response.json()['human_review_required'] is True
    assert response.json()['mode'] in {'deterministic-demo', 'live-groq'}

def test_gap_lifecycle_rejects_invalid_transition_and_accepts_valid_transition():
    invalid = client.patch('/api/v1/gaps/GAP-1042/status', json={'status': 'Closed'})
    assert invalid.json()['status'] == 'invalid_transition'
    valid = client.patch('/api/v1/gaps/GAP-1042/status', json={'status': 'Under Review', 'comment': 'Compliance manager triage'})
    assert valid.json()['status'] == 'updated'
    assert valid.json()['gap']['status'] == 'Under Review'

def test_demo_reset_restores_seed_records():
    client.patch('/api/v1/gaps/GAP-1042/status', json={'status': 'Under Review'})
    response = client.post('/api/v1/demo/reset')
    assert response.json()['status'] == 'reset'
    assert response.json()['documents'] == 3
    assert response.json()['evidence'] == 3
    assert response.json()['agent_runs'] == 1
    assert response.json()['gaps'] == 4
    assert client.get('/api/v1/gaps').json()['items'][0]['status'] == 'Open'

def test_change_analysis_returns_related_records():
    payload = client.get('/api/v1/changes').json()
    assert payload['previous']['document_id'] == 'DOC-002'
    assert payload['current']['document_id'] == 'DOC-001'
    assert payload['summary']['review_required'] == 2
    assert payload['items'][0]['related_obligations'] == ['OBL-007']
    assert payload['items'][0]['related_controls'] == ['CTL-003']
    assert payload['items'][0]['related_evidence'] == ['EVD-001']

def test_clear_and_restore_demo_data():
    cleared = client.delete('/api/v1/demo/data')
    assert cleared.json()['status'] == 'cleared'
    assert client.get('/api/v1/documents').json()['total'] == 0
    assert client.get('/api/v1/gaps').json()['total'] == 0
    assert client.get('/api/v1/controls').json() == []
    assert client.get('/api/v1/obligations').json()['total'] == 0
    assert client.get('/api/v1/dashboard').json()['kpis']['regulations'] == 0
    restored = client.post('/api/v1/demo/reset')
    assert restored.json()['status'] == 'reset'
    assert restored.json()['documents'] == 3
    assert len(client.get('/api/v1/controls').json()) == 4

def test_remediation_requires_demo_manager_role():
    response = client.post('/api/v1/remediation/GAP-1042/approve', headers={'X-Demo-Role': 'viewer'})
    assert response.status_code == 403


def test_assessment_uses_uploaded_document_content_when_available():
    upload = client.post('/api/v1/documents/upload', files={'file': ('quarterly-certification.txt', b'Quarterly regulatory submission is missing the certification page and signature evidence.', 'text/plain')})
    assert upload.status_code == 200
    document_id = upload.json()['id']
    assessment = client.post('/api/v1/assessments', json={'scope':'Quarterly regulatory reporting','business_unit':'Retail Banking'}).json()
    assert 'missing' in assessment['result']['gap'].lower()
    assert assessment['result']['source_document'] == document_id


def test_change_analysis_uses_stored_document_text_not_seed_data():
    upload = client.post('/api/v1/documents/upload', files={'file': ('report-v3.txt', b'New regulatory rule requires certification before submission and independent review of quarterly returns.', 'text/plain')})
    assert upload.status_code == 200
    payload = client.get('/api/v1/changes').json()
    matched = any('independent review' in item['new'].lower() for item in payload['items'])
    assert matched is True


def test_durable_workflow_checkpoint_is_persisted_and_recoverable():
    response = client.post('/api/v1/assessments', json={'scope':'Quarterly certification evidence', 'business_unit':'Retail Banking'})
    assessment = response.json()
    checkpoint = client.get(f"/api/v1/assessments/{assessment['id']}/checkpoint").json()
    assert checkpoint['status'] in {'completed', 'ready'}
    assert checkpoint['assessment_id'] == assessment['id']
    assert checkpoint['state']['review_required'] is True


def test_vector_search_contract_reports_optional_capability():
    response = client.get('/api/v1/search', params={'q': 'certification', 'limit': 3})
    assert response.status_code == 200
    payload = response.json()
    assert 'embedding_available' in payload
    assert payload['mode'] in {'lexical', 'vector', 'hybrid'}


def test_detail_routes_expose_object_level_metadata():
    gap = client.get('/api/v1/gaps/GAP-1042').json()
    assert gap['id'] == 'GAP-1042'
    assert gap['severity'] == 'Critical'

    obligation = client.get('/api/v1/obligations/OBL-007').json()
    assert obligation['id'] == 'OBL-007'
    assert 'certify' in obligation['statement'].lower()
