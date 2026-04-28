from datetime import timedelta
from typing import Any

from django.core.management.base import BaseCommand
from django.utils import timezone

from core_spoton.api.models import StatusReport


class Command(BaseCommand):
    help = "Clears old status reports for spots to ensure status is up to date and not outdate"

    def handle(self, *args: Any, **options: Any) -> None:
        time_threshold = timezone.now() + timedelta(hours=2)
        count, _ = StatusReport.objects.filter(timestamp__lte=time_threshold).delete()
        self.stdout.write(self.style.SUCCESS(f"Successfully cleared {count} status reports"))
