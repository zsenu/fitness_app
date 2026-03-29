from datetime                   import date
from rest_framework             import serializers

from django.contrib.auth.models import User
from .models                    import UserProfile
from .models                    import HealthLog
from .models                    import FoodItem
from .models                    import FoodLog
from .models                    import StrengthExercise
from .models                    import StrengthSet
from .models                    import StrengthTraining
from .models                    import CardioExercise
from .models                    import CardioSet
from .models                    import CardioTraining

"""
User-related serializers
"""
class RegisterSerializer(serializers.ModelSerializer):
    username       =    serializers.CharField()
    email          =   serializers.EmailField()
    password       =    serializers.CharField(write_only = True)
    gender         =  serializers.ChoiceField(choices = UserProfile.GENDER_CHOICES)
    birth_date     =    serializers.DateField()
    height         = serializers.IntegerField()
    current_weight =   serializers.FloatField()
    target_weight  =   serializers.FloatField()
    target_date    =    serializers.DateField()

    class Meta:
        model  = User
        fields = [
            'username',
            'email',
            'password',
            'gender',
            'birth_date',
            'height',
            'current_weight',
            'target_weight',
            'target_date',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_birth_date(self, value):
        if value > date(date.today().year - 18, date.today().month, date.today().day):
            raise serializers.ValidationError("User must be at least 18 years old.")
        return value

    def create(self, validated_data):
        profile_data = {
            key: validated_data.pop(key)
            for key in [
                'gender',
                'birth_date',
                'height',
                'current_weight',
                'target_weight',
                'target_date',
            ]
        }

        user = User.objects.create_user(
            username = validated_data['username'],
            email    = validated_data['email'],
            password = validated_data['password']
        )

        UserProfile.objects.create(user = user, **profile_data)

        return user

class UserProfileSerializer(serializers.ModelSerializer):
    username       =    serializers.CharField(source = 'user.username', read_only = True)
    email          =    serializers.CharField(source = 'user.email',    read_only = True)
    user_id        = serializers.IntegerField(source = 'user.id',       read_only = True)
    current_weight =   serializers.FloatField()
    target_weight  =   serializers.FloatField()
    target_date    =    serializers.DateField()

    class Meta:
        model  = UserProfile
        fields = [
            'user_id', 'username', 'email',
            'gender', 'birth_date', 'height',
            'current_weight', 'target_weight', 'target_date'
        ]
        read_only_fields = [
            'user_id', 'username', 'email', 'id',
            'gender', 'birth_date', 'height'
        ]

# NEEDS IMPLEMENTATION
class HealthLogSerializer(serializers.ModelSerializer):
    class Meta:
        model  = HealthLog
        fields = '__all__'

"""
Food-related serializers
"""
class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FoodItem
        fields = '__all__'

    def validate(self, data):
        instance = getattr(self, 'instance', None)

        fat           = data.get('fat',           instance.fat           if instance else None)
        carbohydrates = data.get('carbohydrates', instance.carbohydrates if instance else None)
        protein       = data.get('protein',       instance.protein       if instance else None)

        if None not in (fat, carbohydrates, protein):
            if fat + carbohydrates + protein > 100:
                raise serializers.ValidationError("Total macronutrients cannot exceed 100 grams.")
        return data

# NEEDS IMPLEMENTATION
class FoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FoodLog
        fields = '__all__'

"""
Strength-related serializers
"""
class StrengthExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StrengthExercise
        fields = '__all__'

# NEEDS IMPLEMENTATION
class StrengthSetSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StrengthSet
        fields = '__all__'

# NEEDS IMPLEMENTATION
class StrengthTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StrengthTraining
        fields = '__all__'

"""
Cardio-related serializers
"""

class CardioExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CardioExercise
        fields = '__all__'

# NEEDS IMPLEMENTATION
class CardioSetSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CardioSet
        fields = '__all__'

# NEEDS IMPLEMENTATION
class CardioTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CardioTraining
        fields = '__all__'
