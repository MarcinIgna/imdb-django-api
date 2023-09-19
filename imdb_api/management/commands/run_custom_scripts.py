from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = 'Run multiple custom scripts'
    
    def handle(self, *args, **kwargs):
        scripts = [
            'python manage.py add_movies',
            'python manage.py add_genres',
            'python manage.py add_trailer',
            'python manage.py add_person',
        ]
        for script in scripts:
            subprocess.run(script, shell=True)