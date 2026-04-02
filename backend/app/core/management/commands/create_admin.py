from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

if os.environ.get('RENDER') is None:
    from dotenv import load_dotenv
    from pathlib import Path
    env_path = Path(__file__).resolve().parents[4] / '.env'
    load_dotenv(dotenv_path = env_path)

class Command(BaseCommand):
    help = 'Create default admin user'

    def handle(self, *args, **kwargs):
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Admin with username {username} created'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin with username {username} already exists'))
