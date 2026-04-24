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
Preset RegisterView and UserProfileView payloads
"""
VALID_USER_PAYLOAD = {
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
    return VALID_USER_PAYLOAD.copy()

def get_password_mismatch_register_payload():
    payload = VALID_USER_PAYLOAD.copy()
    payload['password2'] = 'DifferentPassword123'
    return payload

def get_invalid_age_register_payload():
    payload = VALID_USER_PAYLOAD.copy()
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

"""
Preset HealthLogView payloads
"""
VALID_HEALTH_LOG_PAYLOAD = {
    'date': str(TODAY),
    'bodyweight': MIN_WEIGHT,
    'hours_slept': MIN_HOURS_SLEPT,
    'liquid_consumed': MIN_LIQUID_CONSUMED
}

"""
Factory methods for HealthLogView payloads
"""

def get_valid_health_log_payload():
    return VALID_HEALTH_LOG_PAYLOAD.copy()

def get_empty_health_log_payload():
    return {
        'date': str(TODAY)
    }

def get_future_date_health_log_payload():
    payload = VALID_HEALTH_LOG_PAYLOAD.copy()
    payload['date'] = str(DAY_AFTER_TOMORROW)
    return payload

def get_invalid_health_log_payload():
    payload = VALID_HEALTH_LOG_PAYLOAD.copy()
    payload['bodyweight'] = MAX_WEIGHT + 10
    return payload

def get_valid_health_log_update_payload():
    payload = {
        'bodyweight': MIN_WEIGHT + 5,
        'hours_slept': MIN_HOURS_SLEPT + 1,
        'liquid_consumed': MIN_LIQUID_CONSUMED + 1
    }
    return payload

def get_invalid_health_log_update_payload():
    payload = {
        'bodyweight': MAX_WEIGHT + 10,
        'hours_slept': MAX_HOURS_SLEPT + 5,
        'liquid_consumed': MAX_LIQUID_CONSUMED + 5
    }
    return payload

"""
Preset FoodItemView payloads
"""
VALID_FOOD_ITEM_PAYLOAD = {
    'name': 'Test Food Item',
    'description': 'This is a test food item with valid calorie and nutrient contents',
    'calories': MIN_CALORIE_CONTENT,
    'fat': MIN_NUTRIENT_CONTENT,
    'carbohydrates': MIN_NUTRIENT_CONTENT,
    'protein': MIN_NUTRIENT_CONTENT
}

TOO_HIGH_NUTRIENTS_FOOD_ITEM_PAYLOAD = {
    'name': 'Test Food Item',
    'description': 'This food item has a total nutrient content of over 100 grams per 100 grams',
    'calories': MIN_CALORIE_CONTENT,
    'fat': Decimal('34.00'),
    'carbohydrates': Decimal('34.00'),
    'protein': Decimal('34.00')
}

"""
Factory methods for FoodItemView payloads
"""
def get_valid_food_item_payload():
    return VALID_FOOD_ITEM_PAYLOAD.copy()

def get_invalid_food_item_payload():
    payload = VALID_FOOD_ITEM_PAYLOAD.copy()
    payload['description'] = 'This food has an invalid calorie content that exceeds the maximum allowed value'
    payload['calories'] = MAX_CALORIE_CONTENT + 100
    return payload

def get_too_high_nutrient_food_item_payload():
    return TOO_HIGH_NUTRIENTS_FOOD_ITEM_PAYLOAD.copy()

def get_missing_name_food_item_payload():
    return {
        'description': 'This food item is missing a name',
        'calories': MIN_CALORIE_CONTENT
    }

def get_missing_calorie_food_item_payload():
    return {
        'name': 'Test Food Item',
        'description': 'This food item is missing calorie content'
    }
