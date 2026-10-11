# RegulaAI Architecture

## MVP scope

The MVP demonstrates one complete, auditable path: a regulatory requirement is selected, applicability and control coverage are evaluated, evidence quality is checked, a deterministic risk is calculated, a remediation proposal is produced, and a human approval is recorded.

The application runs in local demo mode without external services. FastAPI owns all business logic and secrets. React calls only versioned API routes. The runtime database is SQLite by default; PostgreSQL/pgvector is the production-like upgrade path.

```mermaid
flowchart LR
  UI[React dashboard] --> API[FastAPI /api/v1]
  API --> DB[(SQLite demo database)]
  API --> RULES[Deterministic rules]
  API --> LLM[Optional Groq service]
  API --> AUDIT[Append-only audit events]
  DOC[Uploaded source] --> INGEST[Validation and ingestion]
  INGEST --> DB
  DB --> WORKFLOW[Assessment workflow]
  WORKFLOW --> RESULT[Gap, risk, remediation]
  RESULT --> UI
```

## Traceability workflow

```mermaid
flowchart TD
  R[Regulation/version] --> O[Obligation with source text]
  O --> A[Applicability: Applicable / Not Applicable / Needs Review]
  A --> C[Control mapping proposal]
  C --> E[Evidence quality and freshness]
  E --> T[Deterministic test]
  T --> G[Gap]
  G --> S[Impact x Likelihood x Criticality]
  S --> M[Remediation proposal]
  M --> H[Human approval]
  H --> AU[Audit event]
```

## Honest limitations

The current implementation uses a local SQLite-compatible persistence layer with synthetic illustrative data. Groq remains optional and server-side only, while the system includes a durable checkpoint fallback and an optional vector search contract for PostgreSQL/pgvector environments. Full external authentication and production-scale vector indexing remain follow-on enhancements beyond the local demo scope.