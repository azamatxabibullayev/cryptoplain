import datetime
from django.core.management.base import BaseCommand
from main.models import Analysis
from django.utils import timezone


class Command(BaseCommand):
    help = 'Delete analyses older than 48 hours'

    def handle(self, *args, **kwargs):
        time_threshold = timezone.now() - datetime.timedelta(hours=48)
        old_analyses = Analysis.objects.filter(created_at__lt=time_threshold)
        count, _ = old_analyses.delete()
        self.stdout.write(f'Successfully deleted {count} analyses older than 48 hours.')
