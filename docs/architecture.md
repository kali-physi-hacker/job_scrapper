Architecture Overview

Components

- API (Django + DRF): REST endpoints for sources, jobs, scoring, applications, automation controls.
- Workers (Celery): Crawl, normalize, score, tailor documents, and submit applications.
- Storage: PostgreSQL (primary), Redis (queues), S3‑compatible for documents.
- Scraping: Playwright service with proxy/session management and evidence capture (DOM/screenshot).
- Frontend: React SPA for admin and user portal.

Data Model (selected)

- Profile, Document, CredentialVault
- Company, JobSource, CrawlJob, RawJobPosting, JobPosting, MatchScore
- Application, ApplicationAttempt
- ProxyProfile, BrowserSession

Flows

1) Crawl: schedule CrawlJob → fetch raw postings → normalize → upsert JobPosting → entity resolve Company → emit events
2) Score: extract features from JD vs Resume → weighted score → persist MatchScore per user
3) Tailor: generate resume variant + cover letter → persist ATS‑safe Document
4) Apply: choose connector or RPA strategy → fill forms/upload → log evidence → update Application/Attempt
5) Learn: track funnel outcomes → tune weights (bandit) → update ScoringModelConfig

Extensibility

- Adapters: `adapters/` implements per‑source fetch + normalize with common interface.
- Strategies: application strategies (api, rpa) implementing `submit(application)`.
- LLM/Embeddings: provider abstraction; run local or cloud; optional.

Security

- Field‑level encryption for credentials; secret rotation; scoped access tokens.
- Role‑based access control; audit logs; PII redaction in logs.
- Config via environment; secrets not committed.

