Setup Guide

Prerequisites

- Python 3.11+
- Node.js 18+
- Redis (for Celery)
- PostgreSQL (recommended) or SQLite (dev)

Backend

1) Create virtualenv and install deps

   python -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt

2) Configure environment

   cp backend/.env.example backend/.env
   # Edit backend/.env for DB and secrets

3) Initialize database

   python backend/manage.py makemigrations
   python backend/manage.py migrate
   python backend/manage.py createsuperuser

4) Run dev server

   python backend/manage.py runserver

Workers

- Start Redis.
- In two terminals:

   celery -A config.celery_app worker -l info
   celery -A config.celery_app beat -l info

Frontend

   cd frontend
   npm install
   npm run dev

Config

- Optionally set `VITE_API_URL` in `frontend/.env` (defaults to http://localhost:8000).
- The UI uses Tailwind with shadcn‑style components. Run `npm install` to fetch Tailwind and related deps.

Apply connectors

- By default, application submissions run in dry-run mode and only log payloads.
- To enable real submissions (use with caution, respect ToS), set `APPLY_REAL=True` in `backend/.env` and restart worker/server.

Seed 100+ sources

- CLI: `python backend/manage.py seed_sources --file data/sources.csv` (ships with 120 placeholder sources; replace with real URLs).
- UI: On `/sources`, paste career board URLs (one per line) into Bulk Add and submit. The platform is auto-detected.

Next Steps

- Add your first JobSource via Django admin at /admin or build a small seeding command.
- Implement adapters in backend/apps/jobs/adapters for Greenhouse/Lever.
- Point frontend API base URL to Django server and build basic views.
