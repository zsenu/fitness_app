from django.core.management.base import BaseCommand
from core.models                 import CustomUser
from decimal                     import Decimal
from datetime                    import date

class Command(BaseCommand):
    help = 'Seeds initial CustomUser data'

    def handle(self, *args, **kwargs):
        items = [
            {
                'username':        'testuser',
                'email':           'testuser@email.com',
                'password':        'TestPassword123',
                'gender':          'M',
                'birth_date':      date(2000, 1, 1),
                'height':          180,
                'starting_weight': Decimal('75.00'),
                'activity_level':  'sedentary',
                'target_weight':   Decimal('70.00'),
                'target_date':     date(2026, 12, 31),
                'target_calories': Decimal('2000.00'),
            },
        ]

        created_count = 0
        updated_count = 0

        for item in items:
            obj, created = CustomUser.objects.get_or_create(
                username = item['username'],
                defaults = {
                    'email':           item['email'],
                    'password':        item['password'],
                    'gender':          item['gender'],
                    'birth_date':      item['birth_date'],
                    'height':          item['height'],
                    'starting_weight': item['starting_weight'],
                    'activity_level':  item['activity_level'],
                    'target_weight':   item['target_weight'],
                    'target_date':     item['target_date'],
                    'target_calories': item['target_calories'],
                },
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: { str(obj) }'))
            else:
                obj.email           = item['email']
                obj.password        = item['password']
                obj.gender          = item['gender']
                obj.birth_date      = item['birth_date']
                obj.height          = item['height']
                obj.starting_weight = item['starting_weight']
                obj.activity_level  = item['activity_level']
                obj.target_weight   = item['target_weight']
                obj.target_date     = item['target_date']
                obj.target_calories = item['target_calories']
                obj.save()

                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated: { str(obj) }'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone. Created: { created_count }, Updated: { updated_count }'
            )
        )
