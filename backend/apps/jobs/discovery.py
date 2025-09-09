from __future__ import annotations
import asyncio
from typing import List, Tuple
import httpx

PLATFORMS: list[tuple[str, callable]] = [
    ("greenhouse", lambda slug: f"https://boards.greenhouse.io/{slug}"),
    ("lever", lambda slug: f"https://jobs.lever.co/{slug}"),
    ("smartrecruiters", lambda slug: f"https://careers.smartrecruiters.com/{slug}"),
    ("workable", lambda slug: f"https://apply.workable.com/{slug}"),
    ("recruitee", lambda slug: f"https://{slug}.recruitee.com"),
    ("breezy", lambda slug: f"https://{slug}.breezy.hr"),
    ("teamtailor", lambda slug: f"https://{slug}.teamtailor.com"),
    ("icims", lambda slug: f"https://careers-{slug}.icims.com"),
]


async def looks_valid_async(client: httpx.AsyncClient, key: str, base_url: str) -> bool:
    try:
        if key == "greenhouse":
            r = await client.get(base_url.rstrip("/") + "/api/public/jobs")
            return r.status_code == 200 and isinstance(r.json(), dict) and "jobs" in (r.json() or {})
        if key == "lever":
            r = await client.get(base_url.rstrip("/") + "?mode=json")
            return r.status_code == 200 and isinstance(r.json(), list)
        if key == "smartrecruiters":
            slug = base_url.rstrip("/").split("/")[-1]
            r = await client.get(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings", params={"limit": 1})
            return r.status_code == 200
        if key == "workable":
            slug = base_url.rstrip("/").split("/")[-1]
            r = await client.get(f"https://apply.workable.com/api/v3/accounts/{slug}/jobs", params={"limit": 1})
            return r.status_code == 200
        if key == "recruitee":
            slug = base_url.split("//")[-1].split("/")[0].split(".")[0]
            r = await client.get(f"https://{slug}.recruitee.com/api/offers/")
            return r.status_code == 200
        if key == "breezy":
            # Many Breezy boards expose /json
            r = await client.get(base_url.rstrip("/") + "/json")
            return r.status_code == 200 and isinstance(r.json(), list)
        if key == "teamtailor":
            # No public JSON; check that the site exists and has jobs in HTML
            r = await client.get(base_url, headers={"accept": "text/html"})
            return r.status_code == 200
        if key == "icims":
            # Check page exists (HTML). iCIMS variations are many; this is heuristic.
            r = await client.get(base_url, headers={"accept": "text/html"})
            return r.status_code == 200
        return False
    except Exception:
        return False


async def find_platform_for_slug(client: httpx.AsyncClient, slug: str) -> Tuple[str, str] | None:
    for key, build in PLATFORMS:
        url = build(slug)
        if await looks_valid_async(client, key, url):
            return (url, key)
    return None


async def discover_all(slugs: List[str], concurrency: int = 20) -> List[Tuple[str, str]]:
    sem = asyncio.Semaphore(concurrency)

    async def task(slug: str) -> Tuple[str, str] | None:
        async with sem:
            async with httpx.AsyncClient(timeout=httpx.Timeout(8.0, connect=4.0), follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}) as client:
                return await find_platform_for_slug(client, slug)

    results: List[Tuple[str, str]] = []
    coros = [task(slug) for slug in slugs]
    for coro in asyncio.as_completed(coros):
        res = await coro
        if res:
            results.append(res)
    return results

