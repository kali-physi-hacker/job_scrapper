Usage Guide — Job Scrapper

Overview

This guide walks through the core flows for discovering jobs, scoring them, preparing tailored applications, and submitting them safely. It also covers bulk discovery and verification via CLI.

Prerequisites

- Backend running (`/api`), Celery worker and beat running, Redis available
- Frontend running (`/`), same browser logged into `/admin` to establish session/CSRF
- Keep `APPLY_REAL=False` in `backend/.env` while testing (dry‑run submissions)

1) Upload Documents (Resumes)

- Go to `/documents`
- Upload a resume file and add keyword metadata (comma‑separated). Keywords improve matching scores.
- You can upload multiple resume variants; the latest can be used as a default on the Jobs page.

2) Add Sources

Option A — Single add
- Page: `/sources`
- Pick a platform key (e.g., greenhouse, lever) and paste the board base URL, then Save.

Option B — Bulk add URLs
- Paste many career board URLs (one per line) into “Bulk Add Sources” and submit. Platform is auto‑detected.

Option C — Discover by company slugs
- Paste company slugs (e.g., stripe, notion, figma) into “Discover by Company Slugs” and click Discover.
- This queues a background task that probes common ATS platforms and creates sources.

3) Crawl Sources

- After sources exist, click “Crawl” next to each source on `/sources`.
- Crawling fetches raw postings and normalizes them into `JobPosting` records with basic skill extraction.

4) Find Matches

Option A — Top Matches
- Page: `/jobs`
- Use filters (title query, location, remote, min score) and click “Top Matches” to compute scores inline and list best matches.

Option B — Score All
- Click “Score All” to queue scoring across all jobs for your user (runs in background via Celery).
- For any job, click “My Score” to compute and view your score immediately.

5) Prepare and Tailor Applications

- On `/jobs`, choose a Default Resume (from `/documents`) and click “Prepare Apply” for a job to create an Application.
- Click “Tailor Cover” to generate an ATS‑safe cover letter tuned to the job’s features.
- You can also tailor a resume variant later from the Applications page.

6) Apply and Monitor

- Page: `/applications`
- Click “Apply” to queue a submission. With `APPLY_REAL=False`, the system performs a dry‑run and logs evidence on the attempt.
- Click “Tailor Cover” or “Tailor Resume” to attach tailored documents to the application.
- Attempts log status and evidence JSON (connector result) for auditing.

Real Submissions (Use with caution)

- Set `APPLY_REAL=True` in `backend/.env` and restart the server/worker to enable actual HTML form submissions.
- Currently supported connectors attempt generic form discovery and submission for Greenhouse/Lever; robust per‑tenant mapping and RPA may still be required.

CLI Workflows (Optional)

- Discover real sources and write CSV
  - `python backend/manage.py discover_sources --companies data/companies.txt --out data/sources.csv --concurrency 40`

- Seed DB from CSV
  - `python backend/manage.py seed_sources --file data/sources.csv`

- Verify existing sources
  - `python backend/manage.py verify_sources`

API Reference (Selected)

- Core
  - `GET /api/core/csrf/` — set CSRF cookie
  - `GET/POST /api/core/documents/?kind=resume` — upload/list documents

- Jobs
  - `GET /api/jobs/postings/` — list postings
  - `GET /api/jobs/postings/top-matches/?q=&location=&remote=&min_score=` — compute best matches for current user
  - `GET /api/jobs/postings/{id}/my-score/` — compute and return score for this job/user
  - `POST /api/jobs/postings/score-all/` — queue scoring
  - `POST /api/jobs/sources/{id}/crawl/` — queue crawl
  - `POST /api/jobs/sources/bulk/` — bulk add sources `{ urls: string[] }`
  - `POST /api/jobs/sources/discover/` — queue discovery `{ slugs: string[], concurrency?: number }`

- Applications
  - `GET /api/applications/applications/` — list your applications
  - `POST /api/applications/applications/prepare/` — create or update app `{ job_id, resume_id?, cover_id? }`
  - `POST /api/applications/applications/{id}/apply/` — queue apply attempt
  - `POST /api/applications/applications/{id}/tailor-cover/` — generate and attach cover letter
  - `POST /api/applications/applications/{id}/tailor-resume/` — generate and attach resume variant

Best Practices

- Respect ToS and robots — disable automation for sites that prohibit it.
- Keep PII minimal; use tailored docs with ATS‑safe formatting.
- Start with dry‑run mode; review evidence logs before enabling real submissions.
- Maintain resume keywords thoughtfully — they drive early scoring.

