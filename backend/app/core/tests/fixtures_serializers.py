from datetime    import date, timedelta
from decimal     import Decimal
from core.models import MIN_AGE,                      MAX_AGE
from core.models import MIN_HEIGHT,                   MAX_HEIGHT
from core.models import MIN_WEIGHT,                   MAX_WEIGHT
from core.models import MIN_TARGET_CALORIES,          MAX_TARGET_CALORIES
from core.models import GENDER_CHOICES

"""
Dates (day after tomorrow because there's a one-day leeway for log dates)
"""
TODAY                = date.today()
DAY_AFTER_TOMORROW   = date.today() + timedelta(days = 2)
CORRECT_BIRTH_DATE   = date.today() - timedelta(days = 365 * (MIN_AGE + 1))
TOO_YOUNG_BIRTH_DATE = date.today() - timedelta(days = 365 * (MIN_AGE - 1))
TOO_OLD_BIRTH_DATE   = date.today() - timedelta(days = 365 * (MAX_AGE + 2))

VALID_CUSTOM_USER_DATA = {
    'username':        'testuser',
    'email':           'testuser@email.com',
    'password':        'TestPassword123',
    'password2':       'TestPassword123',
    'gender':          GENDER_CHOICES[0][0],
    'birth_date':      CORRECT_BIRTH_DATE,
    'height':          MIN_HEIGHT,
    'starting_weight': MAX_WEIGHT,
    'target_weight':   MIN_WEIGHT,
    'target_date':     DAY_AFTER_TOMORROW,
    'target_calories': MIN_TARGET_CALORIES
}

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
    data['target_weight']   = MIN_WEIGHT - 1
    data['target_date']     = TODAY
    data['target_calories'] = MAX_TARGET_CALORIES + 1
    return data
