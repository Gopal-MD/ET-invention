# Development Progress

## Completed

- React/Vite enterprise shell and responsive dashboard.
- FastAPI API with health, dashboard, obligations, controls, evidence, documents, gaps, assessments, changes, assistant, remediation, agent activity, and audit routes.
- Deterministic risk severity calculation and traceable assessment result.
- Upload validation, runtime document records, audit events, and human remediation approval.
- SQLite persistence for documents/audit events, backend-enforced gap lifecycle transitions, and demo reset.
- Optional server-side Groq boundary with explicit deterministic fallback.
- Real TXT, PDF, and DOCX extraction with stable chunk IDs and PDF page provenance.
- API-backed navigation views for documents, obligations, controls, evidence, gaps, changes, agents, audit events, settings, and assessments.
- Persisted assessment workflow records with stage-history list/detail APIs and explicit review-paused stages.
- Frontend production build and backend automated tests.

## Verified commands

- `python -m pytest -q`: 20 passed.
- `npm run build`: passed.
- Live API smoke test: health, configuration, documents, and assistant routes returned successfully.

## Remaining work

- Wire persisted assessment records fully into the ORM and add resumable checkpoints.
- Persist extracted chunks in normalized ORM storage and add embedding retrieval.
- Add durable LangGraph orchestration and retry/idempotency controls.
- Add dedicated detail pages and typed API client modules.
- Add PostgreSQL/pgvector retrieval and LangGraph orchestration.
- Add browser-level accessibility and responsive tests.