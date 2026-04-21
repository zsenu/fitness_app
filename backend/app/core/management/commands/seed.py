from django.core.management.base import BaseCommand
from django.core import management

class Command(BaseCommand):
    help = 'Runs all seed commands'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...\n'))

        seed_commands = [
            'seed_food_items',
            'seed_custom_users',
            'seed_health_logs',
            'seed_muscle_groups',
            'seed_strength_exercises',
            'seed_cardio_exercises',
            'seed_food_logs',
            'seed_strength_logs',
            'seed_cardio_logs'
        ]

        for cmd in seed_commands:
            self.stdout.write(f'Running {cmd}...')
            management.call_command(cmd)

        self.stdout.write(self.style.SUCCESS('\nSeeding completed successfully.'))
