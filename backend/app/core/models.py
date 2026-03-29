from django.db                  import models
from django.core.validators     import MinValueValidator, MaxValueValidator
from django.core.exceptions     import ValidationError
from django.contrib.auth.models import User

"""
UserProfile is an extension of the standard User model provided by Django
"""
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user           = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'profile', primary_key = True)
    gender         =     models.CharField(max_length = 1, choices = GENDER_CHOICES)
    birth_date     =     models.DateField()
    height         =  models.IntegerField(validators = [MinValueValidator(140), MaxValueValidator(240)])
    current_weight =    models.FloatField(validators = [MinValueValidator(40),  MaxValueValidator(140)])
    target_weight  =    models.FloatField(validators = [MinValueValidator(40),  MaxValueValidator(140)])
    target_date    =     models.DateField()

    def __str__(self):
        return f'{self.user.username}\'s profile'

"""
Health logs contain miscellaneous health-related data
"""
# NEEDS IMPLEMENTATION
class HealthLog(models.Model):
    pass

"""
Models related to food entries
"""
class FoodItem(models.Model):
    name          =  models.CharField(max_length = 255, unique = True)
    description   =  models.CharField(max_length = 255, blank = True)
    calories      = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(2000)])
    fat           = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(100)])
    carbohydrates = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(100)])
    protein       = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.name

# NEEDS IMPLEMENTATION
class FoodLog(models.Model):
    pass

"""
Models related to strength training
"""
class StrengthExercise(models.Model):
    ALLOWED_MUSCLE_GROUPS = [
        'chest', 'back', 'abdominals',
        'shoulders', 'biceps', 'triceps',
        'glutes', 'quadriceps', 'hamstrings', 'calves',
    ]

    name                 = models.CharField(max_length = 255, unique = True)
    description          = models.CharField(max_length = 255, blank = True)
    target_muscle_groups = models.JSONField(default = list)

    def clean(self):
        super.clean()

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

class StrengthTraining(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'strength_trainings')
    date = models.DateField()

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f'Strength training for {self.user.username} on {self.date}'

class StrengthSet(models.Model):
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
class CardioExercise(models.Model):
    name                =  models.CharField(max_length = 255, unique = True)
    description         =  models.CharField(max_length = 255, blank = True)
    calories_per_minute = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(50)])

    def __str__(self):
        return self.name

class CardioTraining(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'cardio_trainings')
    date = models.DateField()
    
    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f'Cardio training for {self.user.username} on {self.date}'

class CardioSet(models.Model):
    training = models.ForeignKey(CardioTraining, on_delete = models.CASCADE, related_name = 'session_sets')
    exercise = models.ForeignKey(CardioExercise, on_delete = models.CASCADE, related_name = 'performed_sets')
    duration = models.IntegerField(validators = [MinValueValidator(1)])
    comment  =  models.CharField(max_length = 255, blank = True)

    def __str__(self):
        return f'Set for {self.exercise.name}'
