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

Next Steps

- Add your first JobSource via Django admin at /admin or build a small seeding command.
- Implement adapters in backend/apps/jobs/adapters for Greenhouse/Lever.
- Point frontend API base URL to Django server and build basic views.

