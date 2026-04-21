from django.core.management.base import BaseCommand
from core.models                 import FoodLog
from core.models                 import FoodEntry
from core.models                 import FoodItem
from core.models                 import CustomUser
from decimal                     import Decimal
from datetime                    import date

class Command(BaseCommand):
    help = 'Seeds initial FoodLog and FoodEntry data'

    def handle(self, *args, **kwargs):
        items = [
            {
                'user': CustomUser.objects.filter(username = 'testuser').first(),
                'date': date(2026, 4, 1),
                'food_entries': [
                    {
                        'meal_type': 'lunch',
                        'food_item': FoodItem.objects.filter(name = 'Chicken breast (raw)').first(),
                        'quantity':  Decimal('150.00')
                    },
                    {
                        'meal_type': 'lunch',
                        'food_item': FoodItem.objects.filter(name = 'Rice (raw)').first(),
                        'quantity':  Decimal('200.00')
                    }
                ]
            }
        ]

        log_created_count   = 0
        entry_created_count = 0
        entry_updated_count = 0

        for item in items:
            log_obj, log_created = FoodLog.objects.get_or_create(
                user = item['user'],
                date = item['date']
            )

            for entry in item['food_entries']:
                entry_obj, entry_created = FoodEntry.objects.get_or_create(
                    parent_log = log_obj,
                    meal_type  = entry['meal_type'],
                    food_item  = entry['food_item'],
                    defaults   = { 'quantity': entry['quantity'] }
                )

                if entry_created:
                    entry_created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created: { str(entry_obj) }'))
                else:
                    entry_updated_count += 1
                    entry_obj.quantity = entry['quantity']
                    entry_obj.save()
                    self.stdout.write(self.style.WARNING(f'Updated: { str(entry_obj) }'))

            if log_created:
                log_created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: { str(log_obj) }'))
            else:
                self.stdout.write(self.style.WARNING(f'Log already exists: { str(log_obj) }'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone. Created { log_created_count } FoodLogs, { entry_created_count } FoodEntries, and updated { entry_updated_count } FoodEntries.'
            )
        )
