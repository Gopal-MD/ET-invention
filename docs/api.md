# API Guide

Base URL: `http://127.0.0.1:8000/api/v1`

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/health` | Runtime and provider mode |
| GET | `/configuration` | Safe provider configuration status |
| GET | `/dashboard` | Dashboard metrics and recent activity |
| GET | `/documents` | Regulatory/source document records |
| GET | `/documents/{document_id}` | Extracted text and provenance chunks for one document |
| POST | `/documents/upload` | Validate and ingest a supported upload |
| GET | `/obligations` | Searchable obligation records |
| GET | `/controls` | Control framework records |
| GET | `/evidence` | Evidence quality records |
| GET | `/gaps` | Filterable gap records |
| POST | `/assessments` | Run the deterministic assessment workflow |
| GET | `/changes` | Version comparison demo |
| POST | `/assistant` | Optional server-side Groq analysis or explicit demo fallback |
| GET | `/agent-runs` | Agent/workflow observability records |
| GET | `/audit-events` | Append-only application audit events |
| POST | `/remediation/{gap_id}/approve` | Record human approval and audit event |
| PATCH | `/gaps/{gap_id}/status` | Enforce the gap lifecycle |
| POST | `/demo/reset` | Restore synthetic records |
| DELETE | `/demo/data` | Clear local application data without deleting source code |

Example assessment:

```json
POST /assessments
{"scope":"Quarterly regulatory reporting","business_unit":"Retail Banking"}
```

Every AI-assisted or deterministic result must remain reviewable. Provider errors are returned as errors; they are not silently converted into live success.