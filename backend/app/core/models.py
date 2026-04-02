from django.db                  import models
from django.core.validators     import MinValueValidator, MaxValueValidator
from django.core.exceptions     import ValidationError
from django.contrib.auth.models import User
from django.utils               import timezone
from datetime                   import timedelta
from django.utils.html          import strip_tags

"""
Abstract models to apply certain behaviors
"""
class StripTagsMixin(models.Model):
    class Meta:
        abstract = True

    def clean(self):
        super().clean()

        for field in self._meta.get_fields():
            value = getattr(self, field.name, None)

            if value is None:
                continue

            if isinstance(field, (models.CharField, models.TextField)):
                setattr(self, field.name, strip_tags(value))

            elif isinstance(field, models.JSONField):
                setattr(self, field.name, self._sanitize_json(value))

    def _sanitize_json(self, value):
        if isinstance(value, str):
            return strip_tags(value)
        elif isinstance(value, list):
            return [self._sanitize_json(item) for item in value]
        elif isinstance(value, dict):
            return {key: self._sanitize_json(val) for key, val in value.items()}
        else:
            return value

class FullCleanMixin(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class BaseLogMixin(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
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

        if self.date > timezone.localdate() + timedelta(days = 1):
            raise ValidationError('Date cannot be in the future.')
        if self.is_empty:
            raise ValidationError('At least one metric must be provided.')
        if self.pk:
            original = self.__class__.objects.get(pk = self.pk)
            if original.date != self.date:
                raise ValidationError('Date cannot be modified.')
            
    def save(self, *args, **kwargs):
        if self.is_empty and self.pk:
            self.delete()
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f'Base log for {self.user.username} on {self.date}'

"""
UserProfile is an extension of the standard User model provided by Django
"""
class UserProfile(StripTagsMixin, FullCleanMixin, models.Model):
    MIN_AGE = 18
    MAX_AGE = 150
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    user            = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'profile', primary_key = True)
    gender          =     models.CharField(max_length = 1, choices = GENDER_CHOICES)
    birth_date      =     models.DateField()
    height          =  models.IntegerField(validators = [MinValueValidator(140), MaxValueValidator(240)])
    starting_weight =    models.FloatField(validators = [MinValueValidator(40),  MaxValueValidator(140)])
    target_weight   =    models.FloatField(validators = [MinValueValidator(40),  MaxValueValidator(140)])
    target_date     =     models.DateField()

    def _calculate_age(self):
        today = timezone.localdate()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def clean(self):
        super().clean()
        
        age = self._calculate_age()

        if age < self.MIN_AGE:
            raise ValidationError(f'User must be at least {self.MIN_AGE} years old.')
        elif age > self.MAX_AGE:
            raise ValidationError(f'Birth date cannot be more than {self.MAX_AGE} years ago.')

    def __str__(self):
        return f'{self.user.username}\'s profile'

"""
Health logs contain miscellaneous health-related data
"""
class HealthLog(FullCleanMixin, BaseLogMixin, models.Model):
    bodyweight      = models.FloatField(validators = [MinValueValidator(40), MaxValueValidator(140)], null = True, blank = True)
    hours_slept     = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(24)], null = True, blank = True)
    liquid_consumed = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(10)], null = True, blank = True)
    
    @property
    def is_empty(self):
        return all([
            self.bodyweight      is None,
            self.hours_slept     is None,
            self.liquid_consumed is None
        ])

    def __str__(self):
        return f'Health log for {self.user.username} on {self.date}'

"""
Models related to food entries
"""
class FoodItem(StripTagsMixin, FullCleanMixin, models.Model):
    name          =  models.CharField(max_length = 255, unique = True)
    description   =  models.CharField(max_length = 255, blank = True)
    calories      = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(2000)])
    fat           = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(100)])
    carbohydrates = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(100)])
    protein       = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(100)])

    def clean(self):
        super().clean()

        if self.fat + self.carbohydrates + self.protein > 100:
            raise ValidationError("Total macronutrients cannot exceed 100 grams.")

    def __str__(self):
        return self.name

class MealType(models.TextChoices):
    BREAKFAST = 'breakfast', 'Breakfast'
    LUNCH     = 'lunch',     'Lunch'
    DINNER    = 'dinner',    'Dinner'
    MISC      = 'misc',      'Miscellaneous'

class FoodLog(StripTagsMixin, BaseLogMixin, models.Model):
    @property
    def is_empty(self):
        return self.entries.count() == 0

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
        total = {'calories': 0, 'fat': 0, 'carbohydrates': 0, 'protein': 0}
        for entry in self.entries.all():
            factor = entry.amount_g / 100
            total['calories']     += entry.food_item.calories      * factor
            total['fat']          += entry.food_item.fat           * factor
            total['carbohydrates']+= entry.food_item.carbohydrates * factor
            total['protein']      += entry.food_item.protein       * factor
        return total

    def _calculate_macros(self, meal_type):
        entries = self.entries.filter(meal_type = meal_type)
        macros = {'calories': 0, 'fat': 0, 'carbohydrates': 0, 'protein': 0}
        for entry in entries:
            factor = entry.amount_g / 100 
            macros['calories']     += entry.food_item.calories      * factor
            macros['fat']          += entry.food_item.fat           * factor
            macros['carbohydrates']+= entry.food_item.carbohydrates * factor
            macros['protein']      += entry.food_item.protein       * factor
        return macros

    def __str__(self):
        return f'Food log for {self.user.username} on {self.date}'

class FoodEntry(models.Model):
    food_log  = models.ForeignKey(FoodLog,  on_delete = models.CASCADE, related_name = 'entries')
    meal_type =  models.CharField(max_length = 31, choices = MealType.choices)
    food_item = models.ForeignKey(FoodItem, on_delete = models.CASCADE)
    quantity  = models.FloatField(validators = [MinValueValidator(0.1)])
    comment   =  models.CharField(max_length = 255, blank = True)

    class Meta:
        constraints = [models.UniqueConstraint(fields = ['food_log', 'meal_type', 'food_item'], name = 'foodentry_unique_entry_per_meal')]

    def __str__(self):
        return f"{self.food_item.name} ({self.quantity}g) for meal type {self.meal_type} of user {self.food_log.user.username} on {self.food_log.date}"

"""
Models related to strength training
"""
class StrengthExercise(StripTagsMixin, FullCleanMixin, models.Model):
    ALLOWED_MUSCLE_GROUPS = [
        'chest', 'back', 'abdominals',
        'shoulders', 'biceps', 'triceps',
        'glutes', 'quadriceps', 'hamstrings', 'calves',
    ]

    name                 = models.CharField(max_length = 255, unique = True)
    description          = models.CharField(max_length = 255, blank = True)
    target_muscle_groups = models.JSONField(default = list)

    def clean(self):
        super().clean()

        target_muscle_groups_to_validate = self.target_muscle_groups
        
        if not isinstance(target_muscle_groups_to_validate, list):
            raise ValidationError('target_muscle_groups must be a list of muscle groups.')
        
        invalid = [v for v in target_muscle_groups_to_validate if v not in self.ALLOWED_MUSCLE_GROUPS]
        if invalid:
            raise ValidationError(
                f'Invalid muscle group(s): {', '.join(invalid)}. '
                f'Allowed values are: {', '.join(self.ALLOWED_MUSCLE_GROUPS)}'
            )

    def __str__(self):
        return self.name

class StrengthTraining(BaseLogMixin, models.Model):
    @property
    def is_empty(self):
        return self.session_sets.count() == 0

    def __str__(self):
        return f'Strength training for {self.user.username} on {self.date}'

class StrengthSet(StripTagsMixin, models.Model):
    training =   models.ForeignKey(StrengthTraining, on_delete = models.CASCADE, related_name = 'session_sets')
    exercise =   models.ForeignKey(StrengthExercise, on_delete = models.CASCADE, related_name = 'performed_sets')
    weight   =   models.FloatField(validators = [MinValueValidator(0.1)])
    reps     = models.IntegerField(validators = [MinValueValidator(1)])
    comment  =    models.CharField(max_length = 255, blank = True)

    def __str__(self):
        return f'Set for {self.exercise.name}'

"""
Models related to cardio training
"""
class CardioExercise(StripTagsMixin, models.Model):
    name                =  models.CharField(max_length = 255, unique = True)
    description         =  models.CharField(max_length = 255, blank = True)
    calories_per_minute = models.FloatField(validators = [MinValueValidator(0.1), MaxValueValidator(50)])

    def __str__(self):
        return self.name

class CardioTraining(BaseLogMixin, models.Model):
    @property
    def is_empty(self):
        return self.session_sets.count() == 0

    def __str__(self):
        return f'Cardio training for {self.user.username} on {self.date}'

class CardioSet(StripTagsMixin, models.Model):
    training = models.ForeignKey(CardioTraining, on_delete = models.CASCADE, related_name = 'session_sets')
    exercise = models.ForeignKey(CardioExercise, on_delete = models.CASCADE, related_name = 'performed_sets')
    duration = models.FloatField(validators = [MinValueValidator(0.1)])
    comment  =  models.CharField(max_length = 255, blank = True)

    def __str__(self):
        return f'Set for {self.exercise.name}'
