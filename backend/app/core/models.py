from django.db                  import models
from django.core.validators     import MinValueValidator, MaxValueValidator
from django.core.exceptions     import ValidationError
from django.contrib.auth.models import User
from django.utils               import timezone
from datetime                   import timedelta
from django.utils.html          import strip_tags

MAX_NAME_LENGTH = 63
MAX_DESCRIPTION_LENGTH = 255
MIN_AGE = 18
MAX_AGE = 150
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female')
]

"""
Abstract models to apply certain behaviors
"""
class StripTagsMixin(models.Model):
    class Meta:
        abstract = True

    def clean(self):
        super().clean()

        for field in self._meta.get_fields():
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
            raise ValidationError({ 'date': 'Date cannot be in the future.' })
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
        parent_log = self.parent_log
        super().delete(*args, **kwargs)
        if parent_log.is_empty:
            parent_log.delete()

class HasNameMixin(models.Model):
    name = models.CharField(max_length = MAX_NAME_LENGTH, unique = True)

    class Meta:
        abstract = True

class HasDescriptionMixin(models.Model):
    description = models.CharField(max_length = MAX_DESCRIPTION_LENGTH, blank = True)

    class Meta:
        abstract = True

"""
UserProfile is an extension of the standard User model provided by Django
"""
class UserProfile(StripTagsMixin, FullCleanMixin, models.Model):
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

        if age < MIN_AGE:
            raise ValidationError({ 'birth_date': f'User must be at least {MIN_AGE} years old.' })
        elif age > MAX_AGE:
            raise ValidationError({ 'birth_date': f'Birth date cannot be more than {MAX_AGE} years ago.' })

    def __str__(self):
        return f'{ self.user.username }\'s profile'

"""
Health logs contain miscellaneous health-related data
"""
class HealthLog(BaseLogMixin, FullCleanMixin, models.Model):
    bodyweight      = models.FloatField(validators = [MinValueValidator(40), MaxValueValidator(140)], null = True, blank = True)
    hours_slept     = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(24)],   null = True, blank = True)
    liquid_consumed = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(10)],   null = True, blank = True)
    
    @property
    def is_empty(self):
        return all([
            self.bodyweight      is None,
            self.hours_slept     is None,
            self.liquid_consumed is None
        ])

    def clean(self):
        super().clean()

        if self.is_empty:
            raise ValidationError({ 'health_log' : 'Health log must contain an entry' })

    def __str__(self):
        return f'Health log for { self.user.username } on { self.date }'

"""
Models related to food entries
"""
class FoodItem(HasNameMixin, HasDescriptionMixin, StripTagsMixin, FullCleanMixin, models.Model):
    calories      = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(2000)])
    fat           = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(100)],  blank = True, default = 0)
    carbohydrates = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(100)],  blank = True, default = 0)
    protein       = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(100)],  blank = True, default = 0)

    def clean(self):
        super().clean()

        self.fat           = self.fat or 0
        self.carbohydrates = self.carbohydrates or 0
        self.protein       = self.protein or 0

        if self.fat + self.carbohydrates + self.protein > 100:
            raise ValidationError({ 'food_item': 'Total macronutrients cannot exceed 100 grams.' })

    def __str__(self):
        return self.name

class MealType(models.TextChoices):
    BREAKFAST = 'breakfast', 'Breakfast'
    LUNCH     = 'lunch',     'Lunch'
    DINNER    = 'dinner',    'Dinner'
    MISC      = 'misc',      'Miscellaneous'

class FoodLog(BaseLogMixin, StripTagsMixin, models.Model):
    @property
    def is_empty(self):
        if not self.pk:
            return False
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
            factor = entry.quantity / 100
            total['calories']     += entry.food_item.calories      * factor
            total['fat']          += entry.food_item.fat           * factor
            total['carbohydrates']+= entry.food_item.carbohydrates * factor
            total['protein']      += entry.food_item.protein       * factor
        return total

    def _calculate_macros(self, meal_type):
        entries = self.entries.filter(meal_type = meal_type)
        macros = {'calories': 0, 'fat': 0, 'carbohydrates': 0, 'protein': 0}
        for entry in entries:
            factor = entry.quantity / 100 
            macros['calories']     += entry.food_item.calories      * factor
            macros['fat']          += entry.food_item.fat           * factor
            macros['carbohydrates']+= entry.food_item.carbohydrates * factor
            macros['protein']      += entry.food_item.protein       * factor
        return macros

    def __str__(self):
        return f'Food log for { self.user.username } on { self.date }'

class FoodEntry(BaseEntryMixin, HasDescriptionMixin, models.Model):
    parent_log  = models.ForeignKey(FoodLog,  on_delete = models.CASCADE, related_name = 'entries')
    meal_type   =  models.CharField(max_length = 31, choices = MealType.choices)
    food_item   = models.ForeignKey(FoodItem, on_delete = models.CASCADE)
    quantity    = models.FloatField(validators = [MinValueValidator(0.1)])

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

class StrengthTraining(BaseLogMixin, models.Model):
    @property
    def is_empty(self):
        if not self.pk:
            return False
        return self.session_sets.count() == 0

    def __str__(self):
        return f'Strength training for { self.user.username } on { self.date }'

class StrengthSet(BaseEntryMixin, HasDescriptionMixin, StripTagsMixin, models.Model):
    parent_log =   models.ForeignKey(StrengthTraining, on_delete = models.CASCADE, related_name = 'session_sets')
    exercise   =   models.ForeignKey(StrengthExercise, on_delete = models.CASCADE, related_name = 'performed_sets')
    weight     =   models.FloatField(validators = [MinValueValidator(0.1)])
    reps       = models.IntegerField(validators = [MinValueValidator(1)])

    def __str__(self):
        return f'Set for { self.exercise.name }'

"""
Models related to cardio training
"""
class CardioExercise(HasNameMixin, HasDescriptionMixin, StripTagsMixin, models.Model):
    calories_per_minute = models.FloatField(validators = [MinValueValidator(0.1), MaxValueValidator(50)])

    def __str__(self):
        return self.name

class CardioTraining(BaseLogMixin, models.Model):
    @property
    def is_empty(self):
        if not self.pk:
            return False
        return self.session_sets.count() == 0

    def __str__(self):
        return f'Cardio training for { self.user.username } on { self.date }'

class CardioSet(BaseEntryMixin, HasDescriptionMixin, StripTagsMixin, models.Model):
    parent_log = models.ForeignKey(CardioTraining, on_delete = models.CASCADE, related_name = 'session_sets')
    exercise   = models.ForeignKey(CardioExercise, on_delete = models.CASCADE, related_name = 'performed_sets')
    duration   = models.FloatField(validators = [MinValueValidator(0.1)])

    def __str__(self):
        return f'Set for { self.exercise.name }'
