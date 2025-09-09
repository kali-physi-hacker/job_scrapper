Features — Deep Job Search & Auto‑Apply

Acquisition

- Source adapters: Greenhouse, Lever (API); Workday, Ashby, Teamtailor (API or scrape);
  generic HTML scraper with schema.org JobPosting; Github Jobs‑like feeds; custom CSV.
- Playwright RPA: JS rendering, stealth profiles, rotating proxies, timing variance.
- Freshness: Sitemaps, ETags, last‑modified headers, and delta crawl windows.

Normalization & Quality

- Canonical schema: company, title, location, remote, description, requirements, skills, tokens.
- Dedupe: Fuzzy URL and content hashing; entity resolution on companies/domains.
- Spam filter: Heuristics for MLM, unpaid, expired, bait‑and‑switch.

Matching & Scoring

- Skill match: resume vs JD token overlap; weighted hard skills; years of experience.
- Semantic similarity: embeddings (provider pluggable); penalize red flags (visa required, relocation).
- Seniority fit: title normalization + level detection; location/remote fit; compensation range matching.
- Feedback loop: Learn weights from outcomes (bandit); per‑user calibration.

Document Tailoring

- Resume variants: section toggles, keyword infusion, ATS‑safe formatting;
  PDF generation; deduplicate buzzwords; quantifiable impact statements.
- Cover letters: role‑specific templates, JD‑anchored paragraphs; tone/length controls.
- Portfolio mapping: auto‑attach best projects/examples matching JD signals.

Application Automation

- ATS connectors: Greenhouse, Lever, SmartRecruiters via APIs; fall back to RPA for Workday/others.
- Form filler: schema→form mapping, upload handlers, validation and screenshot evidence.
- Account handling: credential vault, MFA prompts, session reuse, anti‑CSRF.
- Rate limits: time windows, randomized delays, geo/IP rotation.

Ops, Safety, Compliance

- Opt‑in and transparency; audit logs; consent receipts.
- Robots/ToS controls; site‑level kill switches; blocklists/allowlists.
- PII minimization; field encryption; role‑based access; retention policies.

Analytics

- Funnel: discovered → qualified → applied → interviewed → offer; drop‑off reasons.
- A/B tests: resume versions, cover letter styles, application strategies.
- Source performance: time‑to‑apply, acceptance rate by source and role.

