from django.db                  import models, transaction
from django.contrib.auth.models import AbstractUser
from django.conf                import settings
from django.core.validators     import MinValueValidator, MaxValueValidator
from django.core.exceptions     import ValidationError
from django.utils               import timezone
from django.utils.html          import strip_tags
from datetime                   import timedelta
from decimal                    import Decimal

"""
Custom user model
"""
MIN_AGE                 = 18
MAX_AGE                 = 150
MIN_HEIGHT              = 140
MAX_HEIGHT              = 240
MIN_WEIGHT              = Decimal('40.00')
MAX_WEIGHT              = Decimal('140.00')
MIN_TARGET_CALORIES     = Decimal('100.00')
MAX_TARGET_CALORIES     = Decimal('10000.00')
DEFAULT_TARGET_CALORIES = Decimal('2000.00')
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female')
]
ACTIVITY_LEVEL_CHOICES = [
    ('sedentary',         'Sedentary (little or no exercise)'),
    ('lightly_active',    'Lightly active (light exercise/sports 1-3 days/week)'),
    ('moderately_active', 'Moderately active (moderate exercise/sports 3-5 days/week)'),
    ('very_active',       'Very active (hard exercise/sports 6-7 days a week)'),
    ('extra_active',      'Extra active (very hard exercise/sports & physical job or 2x training)')
]
ACTIVITY_MULTIPLIERS = {
    'sedentary':         1.2,
    'lightly_active':    1.375,
    'moderately_active': 1.55,
    'very_active':       1.725,
    'extra_active':      1.9
}

class CustomUser(AbstractUser):
    gender          =     models.CharField(max_length = 1,  choices = GENDER_CHOICES)
    birth_date      =     models.DateField()
    height          =  models.IntegerField(                                     validators = [MinValueValidator(MIN_HEIGHT),          MaxValueValidator(MAX_HEIGHT)])
    starting_weight =  models.DecimalField(max_digits = 8,  decimal_places = 2, validators = [MinValueValidator(MIN_WEIGHT),          MaxValueValidator(MAX_WEIGHT)])
    activity_level  =     models.CharField(max_length = 31, choices = ACTIVITY_LEVEL_CHOICES, default = 'sedentary')
    target_weight   =  models.DecimalField(max_digits = 8,  decimal_places = 2, validators = [MinValueValidator(MIN_WEIGHT),          MaxValueValidator(MAX_WEIGHT)])
    target_date     =     models.DateField()
    target_calories =  models.DecimalField(max_digits = 8,  decimal_places = 2, validators = [MinValueValidator(MIN_TARGET_CALORIES), MaxValueValidator(MAX_TARGET_CALORIES)], default = DEFAULT_TARGET_CALORIES)

    @property
    def bmr(self):
        age = self._calculate_age()
        if self.gender == 'M':
            return 10 * float(self.starting_weight) + 6.25 * self.height - 5 * age + 5
        else:
            return 10 * float(self.starting_weight) + 6.25 * self.height - 5 * age - 161
        
    @property
    def tdee(self):
        multiplier = ACTIVITY_MULTIPLIERS.get(self.activity_level, 1.2)
        return self.bmr * multiplier

    def _calculate_age(self):
        today = timezone.localdate()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def clean(self):
        super().clean()

        errors = {}
        
        if self.birth_date is not None:
            age = self._calculate_age()
            if age < MIN_AGE:
                errors['birth_date'] = f'User must be at least { MIN_AGE } years old.'
            elif age > MAX_AGE:
                errors['birth_date'] = f'User cannot be older than { MAX_AGE } years.'
        
        if self.target_date is not None:
            if self.target_date <= timezone.localdate():
                errors['target_date'] = 'Target date must be in the future.'
            elif self.target_date > timezone.localdate() + timedelta(days = 365 * 100):
                errors['target_date'] = 'Target date cannot be more than 100 years in the future.'

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{ self.username }\'s profile'

"""
Abstract models to apply certain behaviors
"""
MAX_NAME_LENGTH         = 63
MAX_DESCRIPTION_LENGTH  = 255

class HasNameMixin(models.Model):
    name = models.CharField(max_length = MAX_NAME_LENGTH, unique = True)

    class Meta:
        abstract = True

class HasDescriptionMixin(models.Model):
    description = models.CharField(max_length = MAX_DESCRIPTION_LENGTH, blank = True)

    class Meta:
        abstract = True

class BaseLogMixin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    date =  models.DateField()

    class Meta:
        abstract    = True
        constraints = [models.UniqueConstraint(fields = ['user', 'date'], name = '%(app_label)s_%(class)s_unique_user_date')]
        ordering    = ['-date']

    @property
    def is_empty(self):
        raise NotImplementedError('Subclasses must implement `is_empty`.')

    def clean(self):
        super().clean()

        if self.date is not None:
            if self.date > timezone.localdate() + timedelta(days = 1):
                raise ValidationError({ 'date': 'Date cannot be more than 1 day in the future.' })
            if self.date < timezone.localdate() - timedelta(days = 90):
                raise ValidationError({ 'date': 'Date cannot be more than 90 days in the past.' })
            if self.pk:
                original = self.__class__.objects.get(pk = self.pk)
                if original.date != self.date:
                    raise ValidationError({ 'date': 'Date cannot be modified.' })
            
    def save(self, *args, **kwargs):
        if self.is_empty and self.pk:
            self.delete()
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f'Base log for { self.user.username } on { self.date }'

class BaseEntryMixin(models.Model):
    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            parent_log = self.parent_log
            super().delete(*args, **kwargs)

            if parent_log.is_empty:
                parent_log.delete()

class StripTagsMixin(models.Model):
    class Meta:
        abstract = True

    def clean(self):
        super().clean()

        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name, None)
                if value is not None:
                    setattr(self, field.name, strip_tags(value))

class FullCleanMixin(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

"""
Health logs contain miscellaneous health-related data
"""
MIN_HOURS_SLEPT     = Decimal('0.00')
MAX_HOURS_SLEPT     = Decimal('24.00')
MIN_LIQUID_CONSUMED = Decimal('0.00')
MAX_LIQUID_CONSUMED = Decimal('10.00')

class HealthLog(BaseLogMixin, FullCleanMixin, models.Model):
    bodyweight      = models.DecimalField(max_digits = 8, decimal_places = 2, validators = [MinValueValidator(MIN_WEIGHT),          MaxValueValidator(MAX_WEIGHT)],          null = True, blank = True)
    hours_slept     = models.DecimalField(max_digits = 8, decimal_places = 2, validators = [MinValueValidator(MIN_HOURS_SLEPT),     MaxValueValidator(MAX_HOURS_SLEPT)],     null = True, blank = True)
    liquid_consumed = models.DecimalField(max_digits = 8, decimal_places = 2, validators = [MinValueValidator(MIN_LIQUID_CONSUMED), MaxValueValidator(MAX_LIQUID_CONSUMED)], null = True, blank = True)
    
    @property
    def is_empty(self):
        return all([
            self.bodyweight      is None,
            self.hours_slept     is None,
            self.liquid_consumed is None
        ])
    
    def clean(self):
        super().clean()

        if self.is_empty and not self.pk:
            raise ValidationError({ 'health_log': 'At least one of the fields must be filled.' })

    def __str__(self):
        return f'Health log for { self.user.username } on { self.date }'

"""
Models related to food entries
"""
MIN_CALORIE_CONTENT      = Decimal('0.00')
MAX_CALORIE_CONTENT      = Decimal('2000.00')
MIN_NUTRIENT_CONTENT     = Decimal('0.00')
MAX_NUTRIENT_CONTENT     = Decimal('100.00')
DEFAULT_NUTRIENT_CONTENT = Decimal('0.00')

class FoodItem(HasNameMixin, HasDescriptionMixin, StripTagsMixin, FullCleanMixin, models.Model):
    calories      = models.DecimalField(max_digits = 8, decimal_places = 2, validators = [MinValueValidator(MIN_CALORIE_CONTENT),  MaxValueValidator(MAX_CALORIE_CONTENT)])
    fat           = models.DecimalField(max_digits = 8, decimal_places = 2, validators = [MinValueValidator(MIN_NUTRIENT_CONTENT), MaxValueValidator(MAX_NUTRIENT_CONTENT)],  blank = True, default = DEFAULT_NUTRIENT_CONTENT)
    carbohydrates = models.DecimalField(max_digits = 8, decimal_places = 2, validators = [MinValueValidator(MIN_NUTRIENT_CONTENT), MaxValueValidator(MAX_NUTRIENT_CONTENT)],  blank = True, default = DEFAULT_NUTRIENT_CONTENT)
    protein       = models.DecimalField(max_digits = 8, decimal_places = 2, validators = [MinValueValidator(MIN_NUTRIENT_CONTENT), MaxValueValidator(MAX_NUTRIENT_CONTENT)],  blank = True, default = DEFAULT_NUTRIENT_CONTENT)

    def clean(self):
        super().clean()

        if self.fat is None:
            self.fat = 0
        if self.carbohydrates is None:
            self.carbohydrates = 0
        if self.protein is None:
            self.protein = 0

        if self.fat + self.carbohydrates + self.protein > 100:
            raise ValidationError({ 'food_item': 'Total macronutrients cannot exceed 100 grams.' })

    def __str__(self):
        return self.name

class MealType(models.TextChoices):
    BREAKFAST = 'breakfast', 'Breakfast'
    LUNCH     = 'lunch',     'Lunch'
    DINNER    = 'dinner',    'Dinner'
    MISC      = 'misc',      'Miscellaneous'

class FoodLog(BaseLogMixin, StripTagsMixin, FullCleanMixin, models.Model):
    @property
    def is_empty(self):
        if not self.pk:
            return False
        return not self.entries.exists()

    @property
    def breakfast_macros(self):
        return self._calculate_macros(MealType.BREAKFAST)

    @property
    def lunch_macros(self):
        return self._calculate_macros(MealType.LUNCH)

    @property
    def dinner_macros(self):
        return self._calculate_macros(MealType.DINNER)

    @property
    def misc_macros(self):
        return self._calculate_macros(MealType.MISC)

    @property
    def total_macros(self):
        return self._calculate_macros(None)

    def _calculate_macros(self, meal_type):
        entries = (self.entries.filter(meal_type = meal_type) if meal_type else self.entries.all()).select_related('food_item')
        macros = {'calories': 0, 'fat': 0, 'carbohydrates': 0, 'protein': 0}
        for entry in entries:
            factor = entry.quantity / Decimal(100)
            food   = entry.food_item

            macros['calories']     += food.calories      * Decimal(factor)
            macros['fat']          += food.fat           * Decimal(factor)
            macros['carbohydrates']+= food.carbohydrates * Decimal(factor)
            macros['protein']      += food.protein       * Decimal(factor)
        return macros

    def __str__(self):
        return f'Food log for { self.user.username } on { self.date }'

MIN_FOOD_ENTRY_QUANTITY = Decimal('0.10')

class FoodEntry(BaseEntryMixin, HasDescriptionMixin, FullCleanMixin, models.Model):
    parent_log  =   models.ForeignKey(FoodLog, on_delete = models.CASCADE, related_name = 'entries')
    meal_type   =    models.CharField(max_length = 31, choices = MealType.choices)
    food_item   =   models.ForeignKey(FoodItem, on_delete = models.CASCADE)
    quantity    = models.DecimalField(max_digits = 8, decimal_places = 2, validators = [MinValueValidator(MIN_FOOD_ENTRY_QUANTITY)])

    class Meta:
        verbose_name_plural = 'Food entries'
        constraints = [models.UniqueConstraint(fields = ['parent_log', 'meal_type', 'food_item'], name = 'foodentry_unique_entry_per_meal')]

    def __str__(self):
        return f"{ self.food_item.name } ({ self.quantity }g) for meal type { self.meal_type } of user { self.parent_log.user.username } on { self.parent_log.date }"

"""
Models related to strength training
"""
class MuscleGroup(HasNameMixin, models.Model):
    def __str__(self):
        return self.name

class StrengthExercise(HasNameMixin, HasDescriptionMixin, StripTagsMixin, FullCleanMixin, models.Model):
    target_muscle_groups = models.ManyToManyField(MuscleGroup, related_name = 'exercises')

    def __str__(self):
        return self.name

class StrengthTraining(BaseLogMixin, FullCleanMixin, models.Model):
    @property
    def is_empty(self):
        if not self.pk:
            return False
        return not self.session_sets.exists()

    def __str__(self):
        return f'Strength training for { self.user.username } on { self.date }'

MIN_EXERCISE_WEIGHT = Decimal('0.00')
MAX_EXERCISE_WEIGHT = Decimal('1000.00')
MIN_EXERCISE_REPS   = 1

class StrengthSet(BaseEntryMixin, HasDescriptionMixin, StripTagsMixin, FullCleanMixin, models.Model):
    parent_log =   models.ForeignKey(StrengthTraining, on_delete = models.CASCADE, related_name = 'session_sets')
    exercise   =   models.ForeignKey(StrengthExercise, on_delete = models.CASCADE, related_name = 'performed_sets')
    weight     = models.DecimalField(max_digits = 8, decimal_places = 2, validators = [MinValueValidator(MIN_EXERCISE_WEIGHT), MaxValueValidator(MAX_EXERCISE_WEIGHT)])
    reps       = models.IntegerField(                                    validators = [MinValueValidator(MIN_EXERCISE_REPS)])

    def __str__(self):
        return f'Set for { self.exercise.name }'

"""
Models related to cardio training
"""
MIN_EXERCISE_CALORIES_BURNED = Decimal('0.10')
MAX_EXERCISE_CALORIES_BURNED = Decimal('50.00')

class CardioExercise(HasNameMixin, HasDescriptionMixin, StripTagsMixin, FullCleanMixin, models.Model):
    calories_per_minute = models.DecimalField(max_digits = 8, decimal_places = 2, validators = [MinValueValidator(MIN_EXERCISE_CALORIES_BURNED), MaxValueValidator(MAX_EXERCISE_CALORIES_BURNED)])

    def __str__(self):
        return self.name

class CardioTraining(BaseLogMixin, FullCleanMixin, models.Model):
    @property
    def is_empty(self):
        if not self.pk:
            return False
        return not self.session_sets.exists()

    def __str__(self):
        return f'Cardio training for { self.user.username } on { self.date }'

MIN_EXERCISE_DURATION = Decimal('0.10')
MAX_EXERCISE_DURATION = Decimal('1440.00')

class CardioSet(BaseEntryMixin, HasDescriptionMixin, StripTagsMixin, FullCleanMixin, models.Model):
    parent_log =   models.ForeignKey(CardioTraining, on_delete = models.CASCADE, related_name = 'session_sets')
    exercise   =   models.ForeignKey(CardioExercise, on_delete = models.CASCADE, related_name = 'performed_sets')
    duration   = models.DecimalField(max_digits = 8, decimal_places = 2, validators = [MinValueValidator(MIN_EXERCISE_DURATION), MaxValueValidator(MAX_EXERCISE_DURATION)])

    def __str__(self):
        return f'Set for { self.exercise.name }'
