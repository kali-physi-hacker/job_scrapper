from django.core.management.base import BaseCommand
from django.db import transaction
import csv
from pathlib import Path
from apps.jobs.models import JobSource
from apps.jobs.detect import detect_platform_and_config


class Command(BaseCommand):
    help = "Seed JobSource entries from data/sources.csv (base_url[,key])"

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='data/sources.csv')

    @transaction.atomic
    def handle(self, *args, **options):
        file = Path(options['file'])
        if not file.exists():
            self.stderr.write(f"File not found: {file}")
            return
        created = 0
        with file.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                base_url = (row.get('base_url') or '').strip()
                if not base_url:
                    continue
                key = (row.get('key') or '').strip()
                auth_config = {}
                if not key:
                    conf = detect_platform_and_config(base_url)
                    key = conf['key']
                    auth_config = conf.get('auth_config', {})
                JobSource.objects.get_or_create(
                    key=key,
                    base_url=base_url,
                    defaults={'enabled': True, 'auth_config': auth_config},
                )
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {created} sources from {file}"))

