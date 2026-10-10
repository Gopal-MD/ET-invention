# RegulaAI

RegulaAI is a locally runnable prototype for traceable banking regulatory compliance intelligence: regulations -> obligations -> controls -> evidence -> tests -> gaps -> risk -> remediation.

## Quick start

### Backend
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The default mode is deterministic local demo mode. Groq credentials are optional, loaded only by FastAPI, and never sent to the browser. Configure `backend/.env` with `GROQ_API_KEY` and `GROQ_MODEL=llama-3.1-8b-instant` to enable the server-side assistant endpoint.

The MVP creates `backend/regulaai.db` automatically using SQLite. This file is ignored by Git and survives backend restarts. To reset the synthetic scenario, call `POST http://127.0.0.1:8000/api/v1/demo/reset` or use the documented API route. PostgreSQL remains the production-like upgrade path.

To clear application data without deleting source files, call `DELETE http://127.0.0.1:8000/api/v1/demo/data`. This empties local records; call the reset route afterward to restore the synthetic demo.

## What is implemented

- Responsive enterprise shell with Overview, obligations, controls, evidence, assessments, gaps, risk, remediation, agent activity, audit trail, and settings views.
- FastAPI `/api/v1` endpoints for health, configuration, dashboard, obligations, controls, gaps, documents, evidence, assessments, change analysis, agent runs, audit events, assistant analysis, and remediation approval.
- Deterministic risk scoring using Impact x Likelihood x Regulatory Criticality with prototype thresholds.
- Source-linked assessment output, explicit missing/insufficient evidence, human review requirement, SQLite-persisted document records, real TXT/PDF/DOCX extraction, and append-only audit events for approvals/uploads.
- Synthetic demo records are labelled as illustrative and are not regulatory advice.

## Limitations

This MVP uses deterministic rules, optional server-side Groq analysis, and SQLite persistence for uploaded documents/audit events. The seeded synthetic dataset remains in process memory, while uploaded source records and audit events survive restarts. LangGraph orchestration, embeddings, SQLAlchemy/Alembic migrations, authentication, dedicated detail routes, and PDF reporting are not yet complete features.
