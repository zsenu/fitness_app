from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create default admin user'

    def handle(self, *args, **kwargs):
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Admin {username} created'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin {username} already exists'))
