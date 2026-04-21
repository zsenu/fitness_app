from django.core.management.base import BaseCommand
from core.models                 import FoodItem
from decimal                     import Decimal

class Command(BaseCommand):
    help = 'Seeds initial FoodItem data'

    def handle(self, *args, **kwargs):
        items = [
            {
                'name':          'Chicken breast (raw)',
                'description':   'Raw skinless chicken breast.',
                'calories':      Decimal('120.00'),
                'protein':       Decimal('23.00'),
                'fat':           Decimal('2.60'),
                'carbohydrates': Decimal('0.00'),
            },
            {
                'name':          'Rice (raw)',
                'description':   'White rice (uncooked).',
                'calories':      Decimal('365.00'),
                'protein':       Decimal('7.10'),
                'fat':           Decimal('0.70'),
                'carbohydrates': Decimal('80.00'),
            },
            {
                'name':          'Apple',
                'description':   'Raw apple with skin.',
                'calories':      Decimal('52.00'),
                'protein':       Decimal('0.30'),
                'fat':           Decimal('0.20'),
                'carbohydrates': Decimal('14.00'),
            },
        ]

        created_count = 0
        updated_count = 0

        for item in items:
            obj, created = FoodItem.objects.get_or_create(
                name = item['name'],
                defaults = {
                    'description':   item['description'],
                    'calories':      item['calories'],
                    'fat':           item['fat'],
                    'carbohydrates': item['carbohydrates'],
                    'protein':       item['protein'],
                },
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: { str(obj) }'))
            else:
                obj.description   = item['description']
                obj.calories      = item['calories']
                obj.fat           = item['fat']
                obj.carbohydrates = item['carbohydrates']
                obj.protein       = item['protein']
                obj.save()

                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated: { str(obj) }'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone. Created: { created_count }, Updated: { updated_count }'
            )
        )
