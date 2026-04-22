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
Preset RegisterSerializer data
"""
VALID_CUSTOM_USER_DATA = {
    'username':        'testuser',
    'email':           'testuser@email.com',
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
Factory methods for CustomUser-related serializers
"""
def get_valid_custom_user_data():
    return VALID_CUSTOM_USER_DATA.copy()

def get_mismatched_password_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['password2'] = 'DifferentPassword123'
    return data

def get_invalid_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['gender']          = 'O'
    data['birth_date']      = TOO_YOUNG_BIRTH_DATE
    data['height']          = MAX_HEIGHT + 1
    data['starting_weight'] = MAX_WEIGHT + 1
    data['activity_level']  = 'invalid_activity_level'
    data['target_weight']   = MIN_WEIGHT - 1
    data['target_date']     = TODAY
    data['target_calories'] = MAX_TARGET_CALORIES + 1
    return data

"""
Preset HealthLogSerializer data
"""
VALID_HEALTH_LOG_DATA = {
    'date':            TODAY,
    'bodyweight':      MIN_WEIGHT,
    'hours_slept':     MIN_HOURS_SLEPT,
    'liquid_consumed': MIN_LIQUID_CONSUMED
}

EMPTY_HEALTH_LOG_DATA = {
    'date': TODAY
}

"""
Factory methods for HealthLogSerializer data
"""
def get_valid_health_log_data():
    return VALID_HEALTH_LOG_DATA.copy()

def get_empty_health_log_data():
    return EMPTY_HEALTH_LOG_DATA.copy()

def get_invalid_health_log_data():
    data = VALID_HEALTH_LOG_DATA.copy()
    data['hours_slept']     = MAX_HOURS_SLEPT + 1
    data['liquid_consumed'] = MAX_LIQUID_CONSUMED + 1
    data['bodyweight']      = MAX_WEIGHT + 1
    return data

"""
Preset FoodItemSerializer data
"""
VALID_FOOD_ITEM_DATA = {
    'name':          'Test Food Item',
    'description':   'A test food item for unit testing.',
    'calories':      MIN_CALORIE_CONTENT  + Decimal('100.00'),
    'fat':           MIN_NUTRIENT_CONTENT + Decimal('10.00'),
    'carbohydrates': MIN_NUTRIENT_CONTENT + Decimal('10.00'),
    'protein':       MIN_NUTRIENT_CONTENT + Decimal('10.00')
}

EMPTY_FOOD_ITEM_DATA = {
    'name': 'Empty Food Item',
    'description': 'A food item with empty nutritional values.',
    'calories': 0
}

"""
Factory methods for FoodItemSerializer data
"""
def get_valid_food_item_data():
    return VALID_FOOD_ITEM_DATA.copy()

def get_empty_food_item_data():
    return EMPTY_FOOD_ITEM_DATA.copy()

def get_invalid_food_item_data():
    data = VALID_FOOD_ITEM_DATA.copy()
    data['calories']      = MIN_CALORIE_CONTENT  - Decimal('0.01')
    data['fat']           = MIN_NUTRIENT_CONTENT - Decimal('0.01')
    data['carbohydrates'] = MIN_NUTRIENT_CONTENT - Decimal('0.01')
    data['protein']       = MIN_NUTRIENT_CONTENT - Decimal('0.01')
    return data

def get_too_high_total_nutrients_food_item_data():
    data = VALID_FOOD_ITEM_DATA.copy()
    data['fat']           = Decimal('33.34')
    data['carbohydrates'] = Decimal('33.34')
    data['protein']       = Decimal('33.34')
    return data

"""
Preset FoodLogSerializer data
"""
VALID_FOOD_LOG_DATA = {
    'date': TODAY
}

"""
Factory methods for FoodLogSerializer data
"""
def get_valid_food_log_data():
    return VALID_FOOD_LOG_DATA.copy()

def get_future_date_food_log_data():
    data = VALID_FOOD_LOG_DATA.copy()
    data['date'] = DAY_AFTER_TOMORROW
    return data

"""
Preset FoodEntrySerializer data
"""
VALID_FOOD_ENTRY_DATA = {
    'meal_type': MealType.BREAKFAST,
    'quantity':  MIN_FOOD_ENTRY_QUANTITY + Decimal('100.00')
}

"""
Factory methods for FoodEntrySerializer data
"""
def get_valid_food_entry_data():
    return VALID_FOOD_ENTRY_DATA.copy()

def get_invalid_food_entry_data():
    data = VALID_FOOD_ENTRY_DATA.copy()
    data['quantity'] = MIN_FOOD_ENTRY_QUANTITY - Decimal('0.01')
    return data

"""
Preset MuscleGroupSerializer data
"""
VALID_MUSCLE_GROUP_DATA = {
    'name': 'Test Muscle Group',
}

"""
Factory methods for MuscleGroupSerializer data
"""
def get_valid_muscle_group_data(custom_name = None):
    data = VALID_MUSCLE_GROUP_DATA.copy()
    if custom_name is not None:
        data['name'] = custom_name
    return data

"""
Preset StrengthExerciseSerializer data
"""
VALID_STRENGTH_EXERCISE_DATA = {
    'name':        'Test Strength Exercise',
    'description': 'A test strength exercise for unit testing.',
}

"""
Factory methods for StrengthExerciseSerializer data
"""
def get_valid_strength_exercise_data():
    return VALID_STRENGTH_EXERCISE_DATA.copy()

"""
Preset StrengthTrainingSerializer data
"""
VALID_STRENGTH_TRAINING_DATA = {
    'date': TODAY
}

"""
Factory methods for StrengthTrainingSerializer data
"""
def get_valid_strength_training_data():
    return VALID_STRENGTH_TRAINING_DATA.copy()

def get_future_date_strength_training_data():
    data = VALID_STRENGTH_TRAINING_DATA.copy()
    data['date'] = DAY_AFTER_TOMORROW
    return data

"""
Preset StrengthSetSerializer data
"""
VALID_STRENGTH_SET_DATA = {
    'weight': MIN_EXERCISE_WEIGHT,
    'reps':   MIN_EXERCISE_REPS
}

"""
Factory methods for StrengthSetSerializer data
"""
def get_valid_strength_set_data():
    return VALID_STRENGTH_SET_DATA.copy()

def get_invalid_strength_set_data():
    data = VALID_STRENGTH_SET_DATA.copy()
    data['weight'] = MIN_EXERCISE_WEIGHT - Decimal('0.01')
    data['reps'] = MIN_EXERCISE_REPS - 1
    return data

"""
Preset CardioExerciseSerializer data
"""
VALID_CARDIO_EXERCISE_DATA = {
    'name':                'Test Cardio Exercise',
    'description':         'A test cardio exercise for unit testing.',
    'calories_per_minute': MIN_EXERCISE_CALORIES_BURNED
}

"""
Factory methods for CardioExerciseSerializer data
"""
def get_valid_cardio_exercise_data():
    return VALID_CARDIO_EXERCISE_DATA.copy()

def get_invalid_cardio_exercise_data():
    data = VALID_CARDIO_EXERCISE_DATA.copy()
    data['calories_per_minute'] = MIN_EXERCISE_CALORIES_BURNED - Decimal('0.01')
    return data

"""
Preset CardioTrainingSerializer data
"""
VALID_CARDIO_TRAINING_DATA = {
    'date': TODAY
}

"""
Factory methods for CardioTrainingSerializer data
"""
def get_valid_cardio_training_data():
    return VALID_CARDIO_TRAINING_DATA.copy()

def get_future_date_cardio_training_data():
    data = VALID_CARDIO_TRAINING_DATA.copy()
    data['date'] = DAY_AFTER_TOMORROW
    return data

"""
Preset CardioSetSerializer data
"""
VALID_CARDIO_SET_DATA = {
    'duration': MIN_EXERCISE_DURATION
}

"""
Factory methods for CardioSetSerializer data
"""
def get_valid_cardio_set_data():
    return VALID_CARDIO_SET_DATA.copy()

def get_invalid_cardio_set_data():
    data = VALID_CARDIO_SET_DATA.copy()
    data['duration'] = MIN_EXERCISE_DURATION - Decimal('0.01')
    return data
