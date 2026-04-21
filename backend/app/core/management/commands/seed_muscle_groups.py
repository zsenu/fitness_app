from django.core.management.base import BaseCommand
from core.models                 import MuscleGroup

class Command(BaseCommand):
    help = 'Seeds default muscle groups'

    def handle(self, *args, **kwargs):
        muscle_groups = [
            'neck',
            'chest',
            'back',
            'shoulders',
            'biceps',
            'triceps',
            'forearms',
            'abdominals',
            'glutes',
            'hamstrings',
            'quadriceps',
            'calves',
        ]

        created_count = 0

        for name in muscle_groups:
            obj, created = MuscleGroup.objects.get_or_create(name = name)

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Entry created: { str(obj) }'))
            else:
                self.stdout.write(f'Entry already exists: { str(obj) }')

        self.stdout.write(
            self.style.SUCCESS(f'\nDone. Created { created_count } muscle groups.')
        )