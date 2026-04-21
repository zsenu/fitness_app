from django.core.management.base import BaseCommand
from core.models                 import HealthLog
from core.models                 import CustomUser
from decimal                     import Decimal
from datetime                    import date

class Command(BaseCommand):
    help = 'Seeds initial HealthLog data'

    def handle(self, *args, **kwargs):
        items = [
            {
                'user':            CustomUser.objects.filter(username = 'testuser').first(),
                'date':            date(2026, 4, 1),
                'bodyweight':      Decimal('74.50'),
                'hours_slept':     Decimal('7.50'),
                'liquid_consumed': Decimal('2.00')
            },
            {
                'user':            CustomUser.objects.filter(username = 'testuser').first(),
                'date':            date(2026, 4, 2),
                'bodyweight':      Decimal('74.00'),
                'hours_slept':     Decimal('7.00'),
                'liquid_consumed': Decimal('2.50')
            }
        ]

        created_count = 0
        updated_count = 0

        for item in items:
            obj, created = HealthLog.objects.get_or_create(
                user = item['user'],
                date = item['date'],
                defaults = {
                    'bodyweight':      item['bodyweight'],
                    'hours_slept':     item['hours_slept'],
                    'liquid_consumed': item['liquid_consumed'],
                },
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: { str(obj) }'))
            else:
                obj.bodyweight      = item['bodyweight']
                obj.hours_slept     = item['hours_slept']
                obj.liquid_consumed = item['liquid_consumed']
                obj.save()

                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated: { str(obj) }'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone. Created: { created_count }, Updated: { updated_count }'
            )
        )
