from rest_framework                 import serializers
from django.core.exceptions         import ValidationError as DjangoValidationError

from django.contrib.auth.models     import User
from core.models                    import UserProfile
from core.models                    import HealthLog
from core.models                    import FoodItem, FoodLog
from core.models                    import StrengthExercise, StrengthSet, StrengthTraining
from core.models                    import CardioExercise,   CardioSet,   CardioTraining

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

    def validate(self, attrs):
        profile_data = { key: attrs[key] for key in [
            'gender', 'birth_date', 'height',
            'starting_weight', 'target_weight', 'target_date'
        ]}

        dummy_profile = UserProfile(**profile_data)

        try:
            dummy_profile.full_clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return attrs

    def create(self, attrs):
        profile_data = { key: attrs.pop(key) for key in [
                'gender', 'birth_date', 'height',
                'starting_weight', 'target_weight', 'target_date'
        ]}

        user = User.objects.create_user(
            username = attrs['username'],
            email    = attrs['email'],
            password = attrs['password']
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
    
    def validate(self, attrs):
        instance = UserProfile(**attrs)
        instance.full_clean()
        return attrs

"""
Health-related serializers
"""
class HealthLogSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    
    class Meta:
        model  = HealthLog
        fields = [
            'id', 'user', 'date',
            'bodyweight', 'hours_slept', 'liquid_consumed'
        ]

    def validate(self, attrs):
        instance = HealthLog(**attrs)
        instance.full_clean()
        return attrs

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

    def validate(self, attrs):
        instance = FoodItem(**attrs)
        instance.full_clean()
        return attrs

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

    def validate(self, attrs):
        instance = StrengthExercise(**attrs)
        instance.full_clean()
        return attrs

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

    def validate(self, attrs):
        instance = StrengthSet(**attrs)
        instance.full_clean()
        return attrs

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
    
    def validate(self, attrs):
        instance = CardioExercise(**attrs)
        instance.full_clean()
        return attrs

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

    def validate(self, attrs):
        instance = CardioSet(**attrs)
        instance.full_clean()
        return attrs

class CardioTrainingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    sets = CardioSetSerializer(many = True, read_only = True)

    class Meta:
        model  = CardioTraining
        fields = [
            'id', 'user', 'date', 'sets'
        ]
