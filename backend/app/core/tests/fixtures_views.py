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
