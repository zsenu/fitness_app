from django.core.management.base import BaseCommand
from core.models                 import StrengthTraining
from core.models                 import StrengthSet
from core.models                 import StrengthExercise
from core.models                 import CustomUser
from decimal                     import Decimal
from datetime                    import date

class Command(BaseCommand):
    help = 'Seeds initial StrengthTraining and StrengthSet data'

    def handle(self, *args, **kwargs):
        items = [
            {
                'user': CustomUser.objects.filter(username = 'testuser').first(),
                'date': date(2026, 4, 1),
                'strength_sets': [
                    {
                        'exercise': StrengthExercise.objects.filter(name = 'Tricep dips').first(),
                        'weight':   Decimal('0.00'),
                        'reps':     12
                    },
                    {
                        'exercise': StrengthExercise.objects.filter(name = 'Push-ups').first(),
                        'weight':   Decimal('0.00'),
                        'reps':     20
                    }
                ]
            }
        ]

        log_created_count   = 0
        entry_created_count = 0
        entry_updated_count = 0

        for item in items:
            log_obj, log_created = StrengthTraining.objects.get_or_create(
                user = item['user'],
                date = item['date']
            )

            for entry in item['strength_sets']:
                entry_obj, entry_created = StrengthSet.objects.get_or_create(
                    parent_log = log_obj,
                    exercise   = entry['exercise'],
                    defaults   = {
                        'weight': entry['weight'],
                        'reps':   entry['reps']
                    }
                )

                if entry_created:
                    entry_created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created: { str(entry_obj) }'))
                else:
                    entry_updated_count += 1
                    entry_obj.weight = entry['weight']
                    entry_obj.reps   = entry['reps']
                    entry_obj.save()
                    self.stdout.write(self.style.WARNING(f'Updated: { str(entry_obj) }'))

            if log_created:
                log_created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: { str(log_obj) }'))
            else:
                self.stdout.write(self.style.WARNING(f'Log already exists: { str(log_obj) }'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone. Created { log_created_count } StrengthTrainings, { entry_created_count } StrengthSets, and updated { entry_updated_count } StrengthSets.'
            )
        )
