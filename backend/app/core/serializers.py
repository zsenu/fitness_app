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
    class Meta:
        model  = User
        fields = [
            'username', 'email', 'password',
            'gender', 'birth_date', 'height',
            'starting_weight', 'target_weight', 'target_date'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_data = {
            key: validated_data.pop(key)
            for key in [
                'gender', 'birth_date', 'height',
                'starting_weight', 'target_weight', 'target_date'
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
    user_id        =          serializers.IntegerField(source = 'user.id',       read_only = True)
    username       =             serializers.CharField(source = 'user.username', read_only = True)
    email          =             serializers.CharField(source = 'user.email',    read_only = True)
    current_weight = serializers.SerializerMethodField()

    def get_current_weight(self, obj):
        latest_log = obj.user.health_logs.filter(measured_weight__isnull = False).first()
        return latest_log.measured_weight if latest_log else obj.starting_weight

    class Meta:
        model  = UserProfile
        fields = [
            'user_id', 'username', 'email',
            'gender', 'birth_date', 'height',
            'starting_weight', 'current_weight', 'target_weight', 'target_date'
        ]
        read_only_fields = [
            'user_id', 'username', 'email', 'id',
            'gender', 'birth_date', 'height'
        ]

"""
Health-related serializers
"""
# NEEDS IMPLEMENTATION
class HealthLogSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    
    class Meta:
        model  = HealthLog
        fields = [
            'id', 'user', 'date',
            'measured_weight', 'sleep_hours', 'consumed_liquid_liters'
        ]
        read_only_fields = [
            'id', 'user'
        ]

    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError('Date cannot be in the future.')
        return value
    
    def validate(self, data):
        instance = getattr(self, 'instance', None)

        measured_weight        = data.get('measured_weight',        instance.measured_weight        if instance else None)
        sleep_hours            = data.get('sleep_hours',            instance.sleep_hours            if instance else None)
        consumed_liquid_liters = data.get('consumed_liquid_liters', instance.consumed_liquid_liters if instance else None)

        if not any([
            measured_weight        is not None,
            sleep_hours            is not None,
            consumed_liquid_liters is not None
        ]):
            raise serializers.ValidationError('At least one health metric must be provided.')
        return data 
"""
Food-related serializers
"""
class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FoodItem
        fields = [
            'id', 'name', 'description',
            'calories', 'fat', 'carbohydrates', 'protein'
        ]

    def validate(self, data):
        fat           = data.get('fat')
        carbohydrates = data.get('carbohydrates')
        protein       = data.get('protein')

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
        fields = [
            'id', 'name', 'description',
            'target_muscle_groups'
        ]

class StrengthSetSerializer(serializers.ModelSerializer):
    exercise = StrengthExerciseSerializer(read_only = True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset = StrengthExercise.objects.all(),
        source = 'exercise',
        write_only = True
    )

    class Meta:
        model  = StrengthSet
        fields = [
            'id', 'training_id', 'exercise',
            'exercise_id', 'weight', 'reps', 'comment'
        ]

class StrengthTrainingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    sets = StrengthSetSerializer(many = True, read_only = True)

    class Meta:
        model  = StrengthTraining
        fields = [
            'id', 'user', 'date', 'sets'
        ]

"""
Cardio-related serializers
"""

class CardioExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CardioExercise
        fields = [
            'id', 'name', 'description',
            'calories_burned_per_minute'
        ]

class CardioSetSerializer(serializers.ModelSerializer):
    exercise = CardioExerciseSerializer(read_only = True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset = CardioExercise.objects.all(),
        source = 'exercise',
        write_only = True
    )

    class Meta:
        model  = CardioSet
        fields = [
            'id', 'training_id', 'exercise',
            'exercise_id', 'duration_minutes', 'comment'
        ]

class CardioTrainingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    sets = CardioSetSerializer(many = True, read_only = True)

    class Meta:
        model  = CardioTraining
        fields = [
            'id', 'user', 'date', 'sets'
        ]
