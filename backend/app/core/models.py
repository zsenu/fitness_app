from django.db                  import models
from django.core.validators     import MinValueValidator, MaxValueValidator
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
