from django.core.management.base import BaseCommand
from api.models import StatusReport
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = "Clears old status reports for spots to ensure status is up to date and not outdate"

    def handle(self, *args, **options):
        time_threshold = timezone.now() + timedelta(hours=2)
        count, _ = StatusReport.objects.filter(timestamp__lte=time_threshold).delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully cleared {count} status reports'))
