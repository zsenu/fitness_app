from datetime    import date, timedelta
from decimal     import Decimal
from core.models import MIN_AGE,                      MAX_AGE
from core.models import MIN_HEIGHT,                   MAX_HEIGHT
from core.models import MIN_WEIGHT,                   MAX_WEIGHT
from core.models import MIN_TARGET_CALORIES,          MAX_TARGET_CALORIES
from core.models import GENDER_CHOICES

from core.models import MIN_HOURS_SLEPT,              MAX_HOURS_SLEPT
from core.models import MIN_LIQUID_CONSUMED,          MAX_LIQUID_CONSUMED

from core.models import MIN_CALORIE_CONTENT,          MAX_CALORIE_CONTENT
from core.models import MIN_NUTRIENT_CONTENT,         MAX_NUTRIENT_CONTENT
from core.models import MIN_FOOD_ENTRY_QUANTITY,      MealType

from core.models import MIN_EXERCISE_WEIGHT,          MAX_EXERCISE_WEIGHT
from core.models import MIN_EXERCISE_REPS

from core.models import MIN_EXERCISE_CALORIES_BURNED, MAX_EXERCISE_CALORIES_BURNED
from core.models import MIN_EXERCISE_DURATION,        MAX_EXERCISE_DURATION

"""
Dates (day after tomorrow because there's a one-day leeway for log dates)
"""
TODAY                = date.today()
DAY_AFTER_TOMORROW   = date.today() + timedelta(days = 2)
CORRECT_BIRTH_DATE   = date.today() - timedelta(days = 365 * (MIN_AGE + 1))
TOO_YOUNG_BIRTH_DATE = date.today() - timedelta(days = 365 * (MIN_AGE - 1))
TOO_OLD_BIRTH_DATE   = date.today() - timedelta(days = 365 * (MAX_AGE + 2))

"""
Preset CustomUser data
"""
VALID_CUSTOM_USER_DATA = {
    'username':        'testuser',
    'email':           'testuser@email.com',
    'password':        'TestPassword123',
    'gender':          GENDER_CHOICES[0][0],
    'birth_date':      CORRECT_BIRTH_DATE,
    'height':          MIN_HEIGHT,
    'starting_weight': MAX_WEIGHT,
    'target_weight':   MIN_WEIGHT,
    'target_date':     DAY_AFTER_TOMORROW,
    'target_calories': MIN_TARGET_CALORIES
}

"""
Factory methods for CustomUser data
"""
def get_valid_custom_user_data():
    return VALID_CUSTOM_USER_DATA.copy()

def get_wrong_gender_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['gender'] = 'O'
    return data

def get_too_young_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['birth_date'] = TOO_YOUNG_BIRTH_DATE
    return data

def get_too_old_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['birth_date'] = TOO_OLD_BIRTH_DATE
    return data

def get_too_short_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['height'] = MIN_HEIGHT - 1
    return data

def get_too_tall_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['height'] = MAX_HEIGHT + 1
    return data

def get_too_light_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['starting_weight'] = MIN_WEIGHT - Decimal('0.01')
    return data

def get_too_heavy_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['starting_weight'] = MAX_WEIGHT + Decimal('0.01')
    return data

def get_too_low_target_weight_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['target_weight'] = MIN_WEIGHT - Decimal('0.01')
    return data

def get_too_high_target_weight_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['target_weight'] = MAX_WEIGHT + Decimal('0.01')
    return data

def get_too_low_target_calories_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['target_calories'] = MIN_TARGET_CALORIES - Decimal('0.01')
    return data

def get_too_high_target_calories_custom_user_data():
    data = VALID_CUSTOM_USER_DATA.copy()
    data['target_calories'] = MAX_TARGET_CALORIES + Decimal('0.01')
    return data

"""
Preset HealthLog data
"""
VALID_HEALTH_LOG_DATA = {
    'date':            TODAY,
    'bodyweight':      MIN_WEIGHT,
    'hours_slept':     MIN_HOURS_SLEPT,
    'liquid_consumed': MIN_LIQUID_CONSUMED
}

EMPTY_HEALTH_LOG_DATA = {
    'date':            TODAY
}

"""
Factory methods for HealthLog data
"""
def get_valid_health_log_data():
    return VALID_HEALTH_LOG_DATA.copy()

def get_empty_health_log_data():
    return EMPTY_HEALTH_LOG_DATA.copy()

def get_future_date_health_log_data():
    data = VALID_HEALTH_LOG_DATA.copy()
    data['date'] = DAY_AFTER_TOMORROW
    return data

def get_too_low_bodyweight_health_log_data():
    data = VALID_HEALTH_LOG_DATA.copy()
    data['bodyweight'] = MIN_WEIGHT - Decimal('0.01')
    return data

def get_too_high_bodyweight_health_log_data():
    data = VALID_HEALTH_LOG_DATA.copy()
    data['bodyweight'] = MAX_WEIGHT + Decimal('0.01')
    return data

def get_too_low_hours_slept_health_log_data():
    data = VALID_HEALTH_LOG_DATA.copy()
    data['hours_slept'] = MIN_HOURS_SLEPT - Decimal('0.01')
    return data

def get_too_high_hours_slept_health_log_data():
    data = VALID_HEALTH_LOG_DATA.copy()
    data['hours_slept'] = MAX_HOURS_SLEPT + Decimal('0.01')
    return data

def get_too_low_liquid_consumed_health_log_data():
    data = VALID_HEALTH_LOG_DATA.copy()
    data['liquid_consumed'] = MIN_LIQUID_CONSUMED - Decimal('0.01')
    return data

def get_too_high_liquid_consumed_health_log_data():
    data = VALID_HEALTH_LOG_DATA.copy()
    data['liquid_consumed'] = MAX_LIQUID_CONSUMED + Decimal('0.01')
    return data

"""
Preset FoodItem data
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
Factory methods for FoodItem data
"""

def get_valid_food_item_data():
    return VALID_FOOD_ITEM_DATA.copy()

def get_empty_food_item_data():
    return EMPTY_FOOD_ITEM_DATA.copy()

def get_too_low_nutrients_food_item_data():
    data = VALID_FOOD_ITEM_DATA.copy()
    data['calories']      = MIN_CALORIE_CONTENT  - Decimal('0.01')
    data['fat']           = MIN_NUTRIENT_CONTENT - Decimal('0.01')
    data['carbohydrates'] = MIN_NUTRIENT_CONTENT - Decimal('0.01')
    data['protein']       = MIN_NUTRIENT_CONTENT - Decimal('0.01')
    return data

def get_too_high_nutrients_food_item_data():
    data = VALID_FOOD_ITEM_DATA.copy()
    data['calories']      = MAX_CALORIE_CONTENT  + Decimal('0.01')
    data['fat']           = MAX_NUTRIENT_CONTENT + Decimal('0.01')
    data['carbohydrates'] = MAX_NUTRIENT_CONTENT + Decimal('0.01')
    data['protein']       = MAX_NUTRIENT_CONTENT + Decimal('0.01')
    return data

def get_too_high_total_nutrients_food_item_data():
    data = VALID_FOOD_ITEM_DATA.copy()
    data['fat']           = MAX_NUTRIENT_CONTENT + Decimal('23.35')
    data['carbohydrates'] = MAX_NUTRIENT_CONTENT + Decimal('23.33')
    data['protein']       = MAX_NUTRIENT_CONTENT + Decimal('23.33')
    return data

"""
Preset FoodLog data
"""
VALID_FOOD_LOG_DATA = {
    'date': TODAY
}

"""
Factory methods for FoodLog data
"""
def get_valid_food_log_data():
    return VALID_FOOD_LOG_DATA.copy()

def get_future_date_food_log_data():
    data = VALID_FOOD_LOG_DATA.copy()
    data['date'] = DAY_AFTER_TOMORROW
    return data

"""
Preset FoodEntry data
"""
VALID_FOOD_ENTRY_DATA = {
    'meal_type': MealType.BREAKFAST,
    'quantity':  MIN_FOOD_ENTRY_QUANTITY + Decimal('100.00')
}

"""
Factory methods for FoodEntry data
"""
def get_valid_food_entry_data():
    return VALID_FOOD_ENTRY_DATA.copy()

def get_too_low_quantity_food_entry_data():
    data = VALID_FOOD_ENTRY_DATA.copy()
    data['quantity'] = MIN_FOOD_ENTRY_QUANTITY - Decimal('0.01')
    return data

"""
Preset MuscleGroup data
"""
VALID_MUSCLE_GROUP_DATA = {
    'name': 'Test Muscle Group',
}

"""
Factory methods for MuscleGroup data
"""
def get_valid_muscle_group_data(custom_name = None):
    data = VALID_MUSCLE_GROUP_DATA.copy()
    if custom_name is not None:
        data['name'] = custom_name
    return data

"""
Preset StrengthExercise data
"""
VALID_STRENGTH_EXERCISE_DATA = {
    'name':        'Test Strength Exercise',
    'description': 'A test strength exercise for unit testing.',
}

"""
Factory methods for StrengthExercise data
"""
def get_valid_strength_exercise_data():
    return VALID_STRENGTH_EXERCISE_DATA.copy()

"""
Preset StrengthTraining data
"""
VALID_STRENGTH_TRAINING_DATA = {
    'date': TODAY
}

"""
Factory methods for StrengthTraining data
"""
def get_valid_strength_training_data():
    return VALID_STRENGTH_TRAINING_DATA.copy()

def get_future_date_strength_training_data():
    data = VALID_STRENGTH_TRAINING_DATA.copy()
    data['date'] = DAY_AFTER_TOMORROW
    return data

"""
Preset StrengthSet data
"""
VALID_STRENGTH_SET_DATA = {
    'weight': MIN_EXERCISE_WEIGHT,
    'reps':   MIN_EXERCISE_REPS
}

"""
Factory methods for StrengthSet data
"""
def get_valid_strength_set_data():
    return VALID_STRENGTH_SET_DATA.copy()

def get_too_low_weight_strength_set_data():
    data = VALID_STRENGTH_SET_DATA.copy()
    data['weight'] = MIN_EXERCISE_WEIGHT - Decimal('0.01')
    return data

def get_too_high_weight_strength_set_data():
    data = VALID_STRENGTH_SET_DATA.copy()
    data['weight'] = MAX_EXERCISE_WEIGHT + Decimal('0.01')
    return data

def get_too_low_reps_strength_set_data():
    data = VALID_STRENGTH_SET_DATA.copy()
    data['reps'] = MIN_EXERCISE_REPS - 1
    return data

"""
Preset CardioExercise data
"""
VALID_CARDIO_EXERCISE_DATA = {
    'name':                'Test Cardio Exercise',
    'description':         'A test cardio exercise for unit testing.',
    'calories_per_minute': MIN_EXERCISE_CALORIES_BURNED
}

"""
Factory methods for CardioExercise data
"""
def get_valid_cardio_exercise_data():
    return VALID_CARDIO_EXERCISE_DATA.copy()

def get_too_low_calories_per_minute_cardio_exercise_data():
    data = VALID_CARDIO_EXERCISE_DATA.copy()
    data['calories_per_minute'] = MIN_EXERCISE_CALORIES_BURNED - Decimal('0.01')
    return data

def get_too_high_calories_per_minute_cardio_exercise_data():
    data = VALID_CARDIO_EXERCISE_DATA.copy()
    data['calories_per_minute'] = MAX_EXERCISE_CALORIES_BURNED + Decimal('0.01')
    return data

"""
Preset CardioTraining data
"""
VALID_CARDIO_TRAINING_DATA = {
    'date': TODAY
}

"""
Factory methods for CardioTraining data
"""
def get_valid_cardio_training_data():
    return VALID_CARDIO_TRAINING_DATA.copy()

def get_future_date_cardio_training_data():
    data = VALID_CARDIO_TRAINING_DATA.copy()
    data['date'] = DAY_AFTER_TOMORROW
    return data

"""
Preset CardioSet data
"""
VALID_CARDIO_SET_DATA = {
    'duration': MIN_EXERCISE_DURATION
}

"""
Factory methods for CardioSet data
"""
def get_valid_cardio_set_data():
    return VALID_CARDIO_SET_DATA.copy()

def get_too_low_duration_cardio_set_data():
    data = VALID_CARDIO_SET_DATA.copy()
    data['duration'] = MIN_EXERCISE_DURATION - Decimal('0.01')
    return data

def get_too_high_duration_cardio_set_data():
    data = VALID_CARDIO_SET_DATA.copy()
    data['duration'] = MAX_EXERCISE_DURATION + Decimal('0.01')
    return data
