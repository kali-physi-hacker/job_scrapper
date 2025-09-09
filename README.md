Job Scrapper — Deep Job Search & Auto‑Apply Platform

Overview

Job Scrapper is a full‑stack system to discover, score, tailor, and auto‑apply to jobs across multiple sources. It optimizes for acceptance probability using structured matching, ATS‑friendly documents, and measured automation. The repo is a monorepo with a Django backend and a React (Vite + TS) frontend.

Important note: “100% acceptance” is not realistic. This project focuses on maximizing acceptance probability ethically and within site terms of service. Automation against sites that prohibit it must be disabled unless explicit permission is obtained.

Key Features

- Multi‑source discovery: APIs where available (e.g., Greenhouse, Lever), scraping via Playwright for others, RSS/feeds, and email parsing.
  - Adapters included: greenhouse, lever, smartrecruiters, workable, recruitee (basic); stubs for ashby, workday.
- Normalization pipeline: Canonical job schema, dedupe, entity resolution (companies/sites), spam and expired posting filtering.
- Matching & scoring: Skill extraction, semantic similarity, rule weights, and learning from outcomes (bandit/weighted heuristics).
- Tailored documents: Role‑aware resume variants, ATS‑optimized formatting, targeted cover letters with evidence from projects.
- Application automation: Connectors for popular ATS and safe RPA fallback with headless browser for forms + uploads.
- Human‑in‑the‑loop: Review queues, one‑click approve/apply, confidence thresholds, and override tools.
- Credential vault: Encrypted storage for portal creds, multi‑factor prompts, and secure secret handling.
- Tracking & analytics: Application pipeline, statuses, reasons, funnel metrics, A/B tests for strategy tweaks.
- Scheduling & retries: Time windows, backoff, IP/agent rotation, CAPTCHA handling hooks.
- Compliance & ethics: Respect robots.txt and ToS options, PII minimization, consent logging, audit trails.

Architecture

- Backend: Django + DRF for APIs; Celery + Redis for background jobs; PostgreSQL for persistence; Playwright for scraping; httpx/BS4 for parsing.
- Frontend: React + Vite + TS; admin + candidate portal; dashboards for sources, queues, and outcomes.
- Services: Pluggable source adapters; pluggable application strategies; LLM provider abstraction for text generation (optional, bring‑your‑own key).

Repo Layout

- backend/ — Django project, Celery workers, adapters, DRF APIs
- frontend/ — React (Vite + TS) SPA
- docs/ — Feature specs, architecture diagrams, data model
- Makefile — Common tasks

Quick Start

1) Backend

- Python 3.11+
- Create venv and install requirements: `python -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt`
- Create `.env` from `backend/.env.example` and set secrets
- Run migrations and dev server: `python backend/manage.py migrate && python backend/manage.py runserver`

2) Celery worker + beat

- `celery -A config.celery_app worker -l info`
- `celery -A config.celery_app beat -l info`

3) Frontend

- Node 18+
- `cd frontend && npm install && npm run dev`

Security & Compliance

- Do not enable scraping/automation for sites that forbid it.
- Store PII and credentials encrypted; restrict access and log usage.
- Provide opt‑in consent and data deletion tools.

Roadmap (High Level)

- v0: Core models, source adapters (Greenhouse/Lever), job pipeline, manual review/apply
- v1: Playwright RPA fallback, tailored docs, scoring, analytics
- v2: Learning loop (bandit), A/B tests, connector marketplace, multi‑tenant

How To Use

- Start here: docs/setup.md — environment and run instructions
- Then follow: docs/usage.md — step‑by‑step UI and API workflows
  - Upload resumes and manage keywords
  - Add sources (single, bulk, or discover by company slugs)
  - Crawl, score, and fetch Top Matches
  - Prepare applications, tailor cover letters/resumes
  - Apply (dry‑run by default) and review attempts and evidence

MVP Runbook

- Backend
  - Create `.env` from `backend/.env.example`. Keep `APPLY_REAL=False` for dry-run submissions.
  - `python -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt`
  - `python backend/manage.py makemigrations && python backend/manage.py migrate`
  - `python backend/manage.py createsuperuser && python backend/manage.py runserver`
  - In separate shells: `celery -A config.celery_app worker -l info` and `celery -A config.celery_app beat -l info`

- Frontend
  - `cd frontend && cp .env.example .env && npm install && npm run dev`
  - Log in at `/admin` to establish a session in the same browser.

- Workflow
  1) Documents: Upload a resume (set keywords) at `/documents`.
  2) Sources: Add a Greenhouse/Lever board and click “Crawl”.
  3) Jobs: Use filters or “Top Matches”, select a default resume, click “Prepare Apply”, then “Tailor Cover”.
  4) Applications: Review prepared/submitted apps and attempt logs (dry-run evidence).

Notes

- Submissions are dry-run until `APPLY_REAL=True`. Use with caution and respect site ToS.
- In dev, media uploads are served via Django when `DEBUG=True`.
4) Seed Sources (120 placeholders)

- `python backend/manage.py seed_sources --file data/sources.csv`
- Or use the Bulk Add form in the Sources page (paste URLs, auto-detects platform).
