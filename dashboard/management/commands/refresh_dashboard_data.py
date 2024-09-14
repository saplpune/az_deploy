from django.core.management.base import BaseCommand
from dashboard.views import load_data, DATA_CACHE_KEY
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Refreshes the dashboard data'

    def handle(self, *args, **options):
        self.stdout.write('Refreshing dashboard data...')
        data = load_data()
        if data:
            cache.set(DATA_CACHE_KEY, data, None)  # Cache without expiration
            self.stdout.write(self.style.SUCCESS('Successfully refreshed dashboard data'))
        else:
            self.stdout.write(self.style.ERROR('Failed to refresh dashboard data'))