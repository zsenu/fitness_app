from django.core.management.base import BaseCommand
from core.models                 import CardioTraining
from core.models                 import CardioSet
from core.models                 import CardioExercise
from core.models                 import CustomUser
from decimal                     import Decimal
from datetime                    import date

class Command(BaseCommand):
    help = 'Seeds initial CardioTraining and CardioSet data'

    def handle(self, *args, **kwargs):
        items = [
            {
                'user': CustomUser.objects.filter(username = 'testuser').first(),
                'date': date(2026, 4, 1),
                'cardio_sets': [
                    {
                        'exercise': CardioExercise.objects.filter(name = 'Stair climbing').first(),
                        'duration': Decimal('30.00')
                    },
                    {
                        'exercise': CardioExercise.objects.filter(name = 'Rowing machine').first(),
                        'duration': Decimal('20.00')
                    }
                ]
            }
        ]

        log_created_count   = 0
        entry_created_count = 0
        entry_updated_count = 0

        for item in items:
            log_obj, log_created = CardioTraining.objects.get_or_create(
                user = item['user'],
                date = item['date']
            )

            for entry in item['cardio_sets']:
                entry_obj, entry_created = CardioSet.objects.get_or_create(
                    parent_log = log_obj,
                    exercise   = entry['exercise'],
                    defaults   = {
                        'duration': entry['duration']
                    }
                )

                if entry_created:
                    entry_created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created: { str(entry_obj) }'))
                else:
                    entry_updated_count += 1
                    entry_obj.duration = entry['duration']
                    entry_obj.save()
                    self.stdout.write(self.style.WARNING(f'Updated: { str(entry_obj) }'))

            if log_created:
                log_created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: { str(log_obj) }'))
            else:
                self.stdout.write(self.style.WARNING(f'Log already exists: { str(log_obj) }'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone. Created { log_created_count } CardioTrainings, { entry_created_count } CardioSets, and updated { entry_updated_count } CardioSets.'
            )
        )
