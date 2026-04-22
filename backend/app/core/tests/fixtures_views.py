from datetime     import timedelta
from django.utils import timezone
from decimal      import Decimal
from core.models  import MIN_AGE,                      MAX_AGE
from core.models  import MIN_HEIGHT,                   MAX_HEIGHT
from core.models  import MIN_WEIGHT,                   MAX_WEIGHT
from core.models  import MIN_TARGET_CALORIES,          MAX_TARGET_CALORIES
from core.models  import GENDER_CHOICES

from core.models  import MIN_HOURS_SLEPT,              MAX_HOURS_SLEPT
from core.models  import MIN_LIQUID_CONSUMED,          MAX_LIQUID_CONSUMED

from core.models  import MIN_CALORIE_CONTENT,          MAX_CALORIE_CONTENT
from core.models  import MIN_NUTRIENT_CONTENT,         MAX_NUTRIENT_CONTENT
from core.models  import MIN_FOOD_ENTRY_QUANTITY,      MealType

from core.models  import MIN_EXERCISE_WEIGHT,          MAX_EXERCISE_WEIGHT
from core.models  import MIN_EXERCISE_REPS

from core.models  import MIN_EXERCISE_CALORIES_BURNED, MAX_EXERCISE_CALORIES_BURNED
from core.models  import MIN_EXERCISE_DURATION,        MAX_EXERCISE_DURATION

"""
Dates (day after tomorrow because there's a one-day leeway for log dates)
"""
TODAY                = timezone.localdate()
DAY_AFTER_TOMORROW   = timezone.localdate() + timedelta(days = 2)
CORRECT_BIRTH_DATE   = timezone.localdate() - timedelta(days = 365 * (MIN_AGE + 1))
TOO_YOUNG_BIRTH_DATE = timezone.localdate() - timedelta(days = 365 * (MIN_AGE - 1))
TOO_OLD_BIRTH_DATE   = timezone.localdate() - timedelta(days = 365 * (MAX_AGE + 2))

"""
Preset RegisterView payloads
"""
VALID_REGISTER_PAYLOAD = {
    'username':        'testuser',
    'email':           'test@email.com',
    'password':        'TestPassword123',
    'password2':       'TestPassword123',
    'gender':          GENDER_CHOICES[0][0],
    'birth_date':      CORRECT_BIRTH_DATE,
    'height':          MIN_HEIGHT,
    'starting_weight': MAX_WEIGHT,
    'activity_level':  'sedentary',
    'target_weight':   MIN_WEIGHT,
    'target_date':     DAY_AFTER_TOMORROW,
    'target_calories': MIN_TARGET_CALORIES
}

"""
Factory methods for RegisterView payloads
"""
PATCHED_TARGET_CALORIES = MIN_TARGET_CALORIES + 100
INVALID_TARGET_CALORIES = MAX_TARGET_CALORIES + 100

def get_valid_register_payload():
    return VALID_REGISTER_PAYLOAD.copy()

def get_password_mismatch_register_payload():
    payload = VALID_REGISTER_PAYLOAD.copy()
    payload['password2'] = 'DifferentPassword123'
    return payload

def get_invalid_age_register_payload():
    payload = VALID_REGISTER_PAYLOAD.copy()
    payload['birth_date'] = TOO_YOUNG_BIRTH_DATE
    return payload

def get_valid_calorie_overwrite_profile_payload():
    payload = {
        'target_calories': PATCHED_TARGET_CALORIES
    }
    return payload

def get_invalid_calorie_overwrite_profile_payload():
    payload = {
        'target_calories': INVALID_TARGET_CALORIES
    }
    return payload

def get_immutable_field_overwrite_profile_payload():
    payload = {
        'username': 'newusername'
    }
    return payload
