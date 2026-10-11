# Structured Implementation Plan

## Goal

Upgrade the working RegulaAI MVP toward a submission-ready compliance platform without breaking the local deterministic demo.

## Milestone 1: Persistence foundation

- [x] Add SQLAlchemy 2.x models for the traceability entities.
- [x] Add an Alembic revision that can initialize SQLite and PostgreSQL-compatible tables.
- Keep the lightweight SQLite runtime adapter as the fallback until the ORM path is wired into every API route.
- Add relationship and foreign-key tests.

**Exit check:** ORM metadata creates successfully in SQLite; Alembic revision applies; current API tests remain green. Complete.

## Milestone 2: Grounded retrieval and ingestion

- [x] Store extracted chunks with stable document/version/location metadata.
- [x] Add lexical retrieval with bounded results.
- [x] Add an optional vector adapter contract for PostgreSQL/pgvector.
- [x] Validate citations against retrieved chunk IDs.

**Exit check:** TXT/PDF/DOCX fixtures retrieve source chunks and unsupported citations are flagged. Complete for lexical fallback.

## Milestone 3: Stateful workflow and governance

- [x] Move assessment stages into typed workflow state.
- [x] Persist assessment stage status, outputs, and review pauses for later inspection.
- [x] Add a durable workflow checkpoint adapter with deterministic fallback logic and optional LangGraph-ready execution hooks.
- [x] Add role-aware demo authorization for consequential actions.

**Exit check:** stage review pauses, persisted assessment records, approval authorization, and durable checkpoint recovery are implemented.

## Milestone 4: Submission surface

- Add dedicated detail routes for documents, obligations, evidence, assessments, gaps, and remediation.
- Add version comparison against stored document versions.
- Add browser-level smoke/accessibility checks.
- Update the feature matrix and demo guide with test evidence.

**Exit check:** all judged workflows are navigable, data-backed, and honest about incomplete capabilities.

## Current status

- MVP UI/API, deterministic assessment, audit approval, data reset, real TXT/PDF/DOCX parsing, durable checkpoints, and optional vector search contracts are implemented.
- This session completes the remaining Milestone 2 and Milestone 3 roadmap work while keeping the local demo deterministic and production-ready when optional services are configured.
- Dedicated detail routes are now exposed for gaps and obligations, and the workflow checkpoint recovery is integrated into the assessment lifecycle.
