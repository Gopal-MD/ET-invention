# Feature Matrix

| Hackathon feature | Status | Evidence |
| --- | --- | --- |
| Regulatory intelligence and ingestion | Implemented but not fully tested | `POST /api/v1/documents/upload`, SQLite records, TXT/PDF/DOCX extraction, stable chunks, upload validation |
| Regulatory change intelligence | Partially implemented | Live `GET /api/v1/changes` view with added/modified/removed summary and review action |
| Obligation extraction | Demo-only | Seeded obligations with source sections; live parsing is not complete |
| Control framework understanding | Partially implemented | `GET /api/v1/controls` and dashboard mappings |
| Regulation-to-control mapping | Demo-only | Seeded obligation-to-control links; review persistence is planned |
| Control effectiveness assessment | Partially implemented | Seeded effectiveness and evidence states |
| Evidence-based assessment | Implemented but not fully tested | Evidence API records distinguish incomplete, partial, stale, and current states; assessment result links missing evidence |
| Gap identification | Implemented and tested | Assessment response and gap register; missing evidence produces a gap |
| Risk prioritization | Implemented and tested | Deterministic score/severity function and boundary tests |
| Remediation recommendations | Partially implemented | Assessment recommendation and approval endpoint |
| Regulatory change impact | Demo-only | Illustrative change records identify affected control/review |
| What-if simulation | Not implemented | Explicitly out of MVP scope |
| Cross-regulation intelligence | Not implemented | Explicitly out of MVP scope |
| Contradiction detection | Not implemented | Explicitly out of MVP scope |

This matrix is intentionally conservative. A navigation item or seeded record is not counted as a complete feature unless the underlying behavior is implemented and testable.