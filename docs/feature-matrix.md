# Feature Matrix

| Hackathon feature | Status | Evidence |
| --- | --- | --- |
| Regulatory intelligence and ingestion | Implemented but not fully tested | `POST /api/v1/documents/upload`, SQLite records, TXT/PDF/DOCX extraction, stable chunks, upload validation |
| Regulatory change intelligence | Implemented for the local runtime | Live `GET /api/v1/changes` compares stored document text and surfaces a reviewable delta |
| Obligation extraction | Implemented for the demo runtime | Seeded obligations are source-linked and available through the public API |
| Control framework understanding | Implemented | `GET /api/v1/controls` and dashboard mappings are live-backed |
| Regulation-to-control mapping | Implemented for the deterministic demo | Seeded obligation-to-control links are persisted within the assessment flow |
| Control effectiveness assessment | Implemented | Seeded effectiveness and evidence states are surfaced through the assessment and dashboard |
| Evidence-based assessment | Implemented and tested | Assessment result is derived from uploaded document content and evaluates evidence gaps |
| Gap identification | Implemented and tested | Assessment response and gap register; missing evidence produces a gap |
| Risk prioritization | Implemented and tested | Deterministic score/severity function and boundary tests |
| Remediation recommendations | Implemented | Assessment recommendation and approval endpoint are wired and audited |
| Regulatory change impact | Implemented | Change records identify affected controls and evidence review requirements |
| What-if simulation | Not implemented | Explicitly out of MVP scope |
| Cross-regulation intelligence | Not implemented | Explicitly out of MVP scope |
| Contradiction detection | Not implemented | Explicitly out of MVP scope |

This matrix is intentionally conservative. A navigation item or seeded record is not counted as a complete feature unless the underlying behavior is implemented and testable.

## Architecture Capabilities

| Capability | Status | Evidence |
| --- | --- | --- |
| SQLAlchemy normalized schema | Implemented and tested | `backend/models.py`, `test_orm.py` |
| Alembic initialization | Implemented and verified | `backend/migrations/versions/0001_traceability_schema.py`, `alembic upgrade head` |
| Lexical retrieval fallback | Implemented and tested | `GET /api/v1/search`, `test_retrieval.py` |
| Typed assessment workflow | Implemented and tested | `backend/workflow.py`, `test_workflow.py` |
| Durable local checkpointing | Implemented | `backend/orchestration.py` and assessment checkpoint endpoint |
| Demo-role authorization | Implemented and tested | `X-Demo-Role`, remediation approval test |
| LangGraph orchestration | Not implemented | Local fallback is deterministic and checkpoint-backed, not external DAG orchestration |
| pgvector embeddings | Partial / contract-level | Optional vector adapter is available; full Postgres deployment is not yet configured |
