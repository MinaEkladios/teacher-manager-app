# TeacherManager

A PWA web application for managing classroom attendance, student profiles, schedules, resources, alerts, reporting, and analytics with secure role-based access.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI (Python 3.12) |
| Frontend | Jinja2 + HTML5 + PWA |
| Database | PostgreSQL + Alembic migrations |
| Cache | Redis |
| Auth | JWT + RBAC (4 roles) |
| APM | Sentry |
| CI/CD | GitHub Actions |
| Deploy | Render (Docker) |

## Roles

| Role | Access |
|------|--------|
| **admin** | Full system access, user management, school config |
| **teacher** | Attendance, student profiles, class management, reports |
| **parent** | View child attendance, alerts, reports |
| **student** | View own attendance, schedule |

## Core Features (must-have)

- Attendance interface (mark, edit, view)
- Student profiles (CRUD, CSV import/export)
- Classes & schedules management
- Automatic absence alerts
- RBAC with 4 roles
- Audit log
- PDF reports (WeasyPrint)
- PWA offline sync

## Nice-to-have

- QR/geo student check-in
- Advanced analytics dashboards
- SMS notifications
- Resource tagging
- Multi-school support

## Quick Start

```bash
# 1. Clone & enter
git clone <repo-url> && cd TeacherManager

# 2. Install dependencies (Poetry)
poetry install

# 3. Copy env
cp .env.example .env
# Edit .env with your database URL, secrets, etc.

# 4. Run migrations
alembic upgrade head

# 5. Start dev server
uvicorn app.main:app --reload --port 8000
```

## Project Structure

```
app/
├── main.py              # FastAPI app factory
├── core/
│   ├── config.py        # Settings (Pydantic)
│   └── security.py      # JWT + hashing
├── api/
│   └── routes.py        # Route definitions
├── models/
│   └── __init__.py      # SQLAlchemy models
├── schemas/
│   └── __init__.py      # Pydantic schemas
└── services/
    └── __init__.py      # Business logic
templates/               # Jinja2 HTML templates
static/                  # CSS, JS, PWA assets
alembic/                 # DB migrations
tests/                   # Pytest test suite
scripts/                 # Utility scripts
```

## Environment Variables

See [.env.example](.env.example) for all required/optional variables.

## License

MIT
