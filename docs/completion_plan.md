# Completion Plan

This plan is intentionally scoped to reliable submission value rather than decorative breadth.

## Priority checklist

- [x] Baseline existing backend tests and frontend production build.
- [x] Document current architecture, API, demo walkthrough, progress, and feature status.
- [x] Remove credential-looking values from example configuration.
- [x] Persist documents and audit events in local SQLite demo mode.
- [x] Enforce gap lifecycle transitions and demo reset.
- [x] Add real TXT, PDF, and DOCX extraction with stable provenance chunks.
- [ ] Persist extracted chunks and expose document detail/preview APIs.
- [ ] Add normalized SQLAlchemy/Alembic schema while preserving SQLite fallback.
- [ ] Persist assessment stage events and resumable workflow state.
- [x] Replace generic frontend views with API-backed record views and loading/error states.
- [ ] Add deterministic version comparison against stored document versions.
- [ ] Add browser-level route/accessibility checks.
- [ ] Add PostgreSQL/pgvector adapter and optional lexical/embedding retrieval.
- [ ] Add LangGraph orchestration only after stage persistence is available.

## Verification rule

A feature is marked complete only when its API behavior has a focused automated test and the frontend build still passes. Groq is never required for ordinary tests or demo startup.
