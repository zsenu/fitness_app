from django.core.management.base import BaseCommand
from core.models                 import StrengthExercise
from core.models                 import MuscleGroup

class Command(BaseCommand):
    help = 'Seeds strength exercises'

    def handle(self, *args, **kwargs):

        items = [
            {
                'name':                 'Tricep dips',
                'description':          'Bodyweight triceps-focused exercise.',
                'target_muscle_groups': ['triceps']
            },
            {
                'name':                 'Push-ups',
                'description':          'Compound bodyweight pushing movement.',
                'target_muscle_groups': ['chest', 'triceps', 'shoulders']
            }
        ]

        for item in items:
            obj, created = StrengthExercise.objects.get_or_create(
                name = item['name'],
                defaults = {
                    'description': item['description'],
                },
            )

            muscle_objs = MuscleGroup.objects.filter(name__in = item['target_muscle_groups'])

            obj.target_muscle_groups.set(muscle_objs)

            obj.save()

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{ action }: { str(obj) }, target_muscle_groups: { ', '.join(item['target_muscle_groups']) }')

        self.stdout.write(self.style.SUCCESS('\nStrength exercises seeded.'))
