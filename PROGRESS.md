# TeacherManager — Progress Tracker

> Paste this file's content into chat when resuming a session.

## Phase 0 — Collect Inputs
- [x] P0.1 — User answered all 12 questions
- [x] P0.2 — Summary table approved

## Phase 1 — Repo Scaffold + Environment Checks
- [x] P1.1 — Created PROGRESS.md, README.md, .env.example
- [x] P1.2 — Created pyproject.toml, requirements.txt
- [ ] P1.3 — Created scripts/check_requirements.ps1, .gitignore; user ran check script

## Phase 2A — Core Basics
- [x] P2A.1 — app/main.py, app/core/config.py
- [x] P2A.2 — All config keys already in .env.example (P1.1)

## Phase 2B — Routes & Authentication
- [x] P2B.1 — app/core/security.py, app/api/routes.py
- [x] P2B.2 — app/models, app/schemas, app/services with core ORM + Pydantic models

## Phase 2C — Migrations & Tests
- [ ] P2C.1 — Alembic skeleton + initial migration
- [ ] P2C.2 — tests/test_health.py, tests/test_auth.py

## Phase 3 — Frontend (Jinja2 + HTML5 + PWA)
- [ ] P3.1 — templates/base.html, templates/index.html, static/css/style.css
- [ ] P3.2 — PWA manifest + service worker

## Phase 4 — Integration, CI, APM
- [ ] P4.1 — DB wiring guidance, Sentry integration
- [ ] P4.2 — .github/workflows/ci.yml, integration test scaffolding

## Phase 5 — Production Prep
- [ ] P5.1 — Dockerfile, docker-compose.yml
- [ ] P5.2 — DEPLOYMENT.md, production checklist

## Phase 6 — Final Acceptance & Handoff
- [ ] P6.1 — Mermaid diagrams (component, sequence, ERD)
- [ ] P6.2 — Release checklist, rollback plan, final deploy
