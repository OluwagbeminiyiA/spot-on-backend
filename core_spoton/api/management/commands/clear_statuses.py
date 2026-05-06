import logging
from datetime import timedelta
from typing import Any

from django.core.management.base import BaseCommand
from django.utils import timezone

from core_spoton.api.models import StatusReport

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Clears old status reports for spots to ensure status is up to date and not outdate"

    def handle(self, *args: Any, **options: Any) -> None:
        time_threshold = timezone.now() + timedelta(hours=2)
        try:
            logger.info("Clearing status reports older than %s", time_threshold)
            count, _ = StatusReport.objects.filter(timestamp__lte=time_threshold).delete()
            logger.info("Cleared status reports count=%s", count)
            self.stdout.write(self.style.SUCCESS(f"Successfully cleared {count} status reports"))
        except Exception:
            logger.exception("Failed to clear status reports")
            raise
