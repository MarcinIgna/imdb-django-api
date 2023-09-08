from django.core.management.base import BaseCommand
from imdb_api.models import Movie

class Command(BaseCommand):
    help = 'Delete all movies from the database'

    def handle(self, *args, **kwargs):
        try:
            # Delete all Movie objects from the database
            Movie.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('All movies have been deleted.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred while deleting movies: {e}'))
