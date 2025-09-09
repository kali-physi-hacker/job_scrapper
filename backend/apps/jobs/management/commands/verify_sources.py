from django.core.management.base import BaseCommand
import httpx
from apps.jobs.models import JobSource


def check_greenhouse(base_url: str) -> bool:
    api = base_url.rstrip('/') + '/api/public/jobs'
    with httpx.Client(timeout=10) as c:
        r = c.get(api)
        return r.status_code == 200 and 'jobs' in (r.json() or {})


def check_lever(base_url: str) -> bool:
    url = base_url.rstrip('/') + '?mode=json'
    with httpx.Client(timeout=10) as c:
        r = c.get(url)
        return r.status_code == 200 and isinstance(r.json(), list)


def check_smartrecruiters(base_url: str, company: str | None) -> bool:
    slug = company
    if not slug and 'smartrecruiters.com' in base_url:
        slug = base_url.rstrip('/').split('/')[-1]
    if not slug:
        return False
    api = f'https://api.smartrecruiters.com/v1/companies/{slug}/postings'
    with httpx.Client(timeout=10) as c:
        r = c.get(api, params={'limit': 1})
        return r.status_code == 200


def check_workable(base_url: str, company: str | None) -> bool:
    slug = company or base_url.rstrip('/').split('/')[-1]
    api = f'https://apply.workable.com/api/v3/accounts/{slug}/jobs'
    with httpx.Client(timeout=10) as c:
        r = c.get(api, params={'limit': 1})
        return r.status_code == 200


def check_recruitee(base_url: str, company: str | None) -> bool:
    host = base_url.split('//')[-1].split('/')[0]
    slug = company or (host.split('.')[0] if host.endswith('.recruitee.com') else None)
    if not slug:
        return False
    api = f'https://{slug}.recruitee.com/api/offers/'
    with httpx.Client(timeout=10) as c:
        r = c.get(api)
        return r.status_code == 200


CHECKERS = {
    'greenhouse': lambda s: check_greenhouse(s.base_url),
    'lever': lambda s: check_lever(s.base_url),
    'smartrecruiters': lambda s: check_smartrecruiters(s.base_url, (s.auth_config or {}).get('company')),
    'workable': lambda s: check_workable(s.base_url, (s.auth_config or {}).get('company')),
    'recruitee': lambda s: check_recruitee(s.base_url, (s.auth_config or {}).get('company')),
    'breezy': lambda s: __import__('httpx').Client(timeout=10).get(s.base_url.rstrip('/') + '/json').status_code == 200,
    'teamtailor': lambda s: __import__('httpx').Client(timeout=10).get(s.base_url).status_code == 200,
    'icims': lambda s: __import__('httpx').Client(timeout=10).get(s.base_url).status_code == 200,
}


class Command(BaseCommand):
    help = 'Verify JobSource records by probing platform APIs (prints valid/invalid)'

    def handle(self, *args, **options):
        ok = 0
        bad = 0
        for s in JobSource.objects.all():
            fn = CHECKERS.get(s.key)
            if not fn:
                self.stdout.write(self.style.WARNING(f'Skipping {s.id} {s.key} (no checker)'))
                continue
            try:
                valid = fn(s)
            except Exception as e:
                valid = False
            if valid:
                ok += 1
                self.stdout.write(self.style.SUCCESS(f'OK {s.key} {s.base_url}'))
            else:
                bad += 1
                self.stdout.write(self.style.ERROR(f'BAD {s.key} {s.base_url}'))
        self.stdout.write(self.style.SUCCESS(f'Valid: {ok}, Invalid: {bad}'))
