from django.core.management.base import BaseCommand
from core.models                 import CardioExercise
from decimal                     import Decimal

class Command(BaseCommand):
    help = 'Seeds cardio exercises'

    def handle(self, *args, **kwargs):

        items = [
            {
                'name':               'Stair climbing',
                'description':        'Cardio exercise that involves climbing stairs.',
                'calories_per_minute': Decimal('8.0'),
            },
            {
                'name':                'Rowing machine',
                'description':         'Cardio exercise performed on a rowing machine.',
                'calories_per_minute': Decimal('10.0'),
            }
        ]

        for item in items:
            obj, created = CardioExercise.objects.get_or_create(
                name = item['name'],
                defaults = {
                    'description':         item['description'],
                    'calories_per_minute': item['calories_per_minute'],
                },
            )

            obj.save()

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{ action }: { str(obj) } - calories_per_minute: { obj.calories_per_minute }')

        self.stdout.write(self.style.SUCCESS('\Cardio exercises seeded.'))
