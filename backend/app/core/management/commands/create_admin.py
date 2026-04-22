from django.core.management.base import BaseCommand
from django.contrib.auth         import get_user_model
import os

if os.environ.get('RENDER') is None:
    from dotenv import load_dotenv
    from pathlib import Path
    env_path = Path(__file__).resolve().parents[4] / '.env'
    load_dotenv(dotenv_path = env_path)

User = get_user_model()

class Command(BaseCommand):
    help = 'Create default admin user'

    def handle(self, *args, **kwargs):
        username        = os.environ.get('ADMIN_USERNAME')
        email           = os.environ.get('ADMIN_EMAIL')
        password        = os.environ.get('ADMIN_PASSWORD')
        gender          = 'M'
        birth_date      = '2000-01-01'
        height          = 180
        starting_weight = 80
        activity_level  = 'bmr'
        target_weight   = 78
        target_date     = '2026-12-31'
        target_calories = 1900

        if not username or not email or not password:
            self.stdout.write(self.style.ERROR('Missing admin credentials in environment variables'))

        if not User.objects.filter(username = username).exists():
            User.objects.create_superuser(
                username, email, password,
                gender = gender, birth_date = birth_date, height = height,
                starting_weight = starting_weight, activity_level = activity_level,
                target_weight = target_weight, target_date = target_date, target_calories = target_calories
            )
            self.stdout.write(self.style.SUCCESS(f'Admin with username { username } created'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin with username { username } already exists'))
