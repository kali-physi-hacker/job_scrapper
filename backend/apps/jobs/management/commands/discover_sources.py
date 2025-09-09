from django.core.management.base import BaseCommand
import asyncio
import httpx
import csv
from pathlib import Path
from apps.jobs.discovery import discover_all


class Command(BaseCommand):
    help = 'Discover real career boards for companies and output CSV: base_url,key'

    def add_arguments(self, parser):
        parser.add_argument('--companies', type=str, required=True, help='Path to text file with one company slug per line')
        parser.add_argument('--out', type=str, default='data/sources.csv', help='Output CSV path')
        parser.add_argument('--concurrency', type=int, default=20)
        parser.add_argument('--limit', type=int, default=0, help='Limit number of companies processed (0 = all)')

    def handle(self, *args, **opts):
        comp_path = Path(opts['companies'])
        out_path = Path(opts['out'])
        concurrency = int(opts['concurrency'])
        limit = int(opts['limit'])
        if not comp_path.exists():
            self.stderr.write(f'Company list not found: {comp_path}')
            return

        slugs = [l.strip() for l in comp_path.read_text().splitlines() if l.strip()]
        if limit > 0:
            slugs = slugs[:limit]

        results = asyncio.run(discover_all(slugs, concurrency=concurrency))
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["base_url", "key"])
            for base_url, key in results:
                writer.writerow([base_url, key])
        self.stdout.write(self.style.SUCCESS(f"Discovered {len(results)} sources → {out_path}"))
