from rest_framework                 import serializers
from django.core.exceptions         import ValidationError as DjangoValidationError

from django.contrib.auth.models     import User
from core.models                    import UserProfile
from core.models                    import HealthLog
from core.models                    import FoodItem,         MealType,    FoodLog,          FoodEntry
from core.models                    import StrengthExercise, StrengthSet, StrengthTraining
from core.models                    import CardioExercise,   CardioSet,   CardioTraining

"""
Abstract serializers to apply certain behaviors
"""
class RelatedToUserSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())

    class Meta:
        abstract = True

class FullCleanSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True

    def validate(self, attrs):
        model_class = self.Meta.model
        instance = model_class(**attrs)
        if getattr(self, 'instance', None):
            instance.pk = self.instance.pk
        instance.full_clean()
        return attrs

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

class UserProfileSerializer(FullCleanSerializer, serializers.ModelSerializer):
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
class HealthLogSerializer(RelatedToUserSerializer, FullCleanSerializer, serializers.ModelSerializer):
    class Meta:
        model  = HealthLog
        fields = [
            'id', 'user', 'date',
            'bodyweight', 'hours_slept', 'liquid_consumed'
        ]

"""
Food-related serializers
"""
class FoodItemSerializer(FullCleanSerializer, serializers.ModelSerializer):
    class Meta:
        model  = FoodItem
        fields = [
            'id', 'name', 'description',
            'calories', 'fat', 'carbohydrates', 'protein'
        ]

# NEEDS IMPLEMENTATION (?)
class FoodEntrySerializer(FullCleanSerializer, serializers.ModelSerializer):
    class Meta:
        model  = FoodEntry
        fields = [
            'id', 'meal_type',
            'food_item', 'quantity', 'comment'
        ]

# NEEDS IMPLEMENTATION (?)
class FoodLogSerializer(RelatedToUserSerializer, FullCleanSerializer, serializers.ModelSerializer):
    entries          = FoodEntrySerializer(many = True, read_only = True)
    breakfast_macros = serializers.SerializerMethodField()
    lunch_macros     = serializers.SerializerMethodField()
    dinner_macros    = serializers.SerializerMethodField()
    misc_macros      = serializers.SerializerMethodField()
    total_macros     = serializers.SerializerMethodField()

    class Meta:
        model  = FoodLog
        fields = [
            'id', 'user', 'date', 'entries',
            'breakfast_macros', 'lunch_macros', 'dinner_macros', 'misc_macros', 'total_macros'
        ]

    def get_breakfast_macros(self, obj):
        return obj.breakfast_macros
    
    def get_lunch_macros(self, obj):
        return obj.lunch_macros
    
    def get_dinner_macros(self, obj):
        return obj.dinner_macros
    
    def get_misc_macros(self, obj):
        return obj.misc_macros
    
    def get_total_macros(self, obj):
        return obj.total_macros

"""
Strength-related serializers
"""
class StrengthExerciseSerializer(FullCleanSerializer, serializers.ModelSerializer):
    class Meta:
        model  = StrengthExercise
        fields = [
            'id', 'name', 'description',
            'target_muscle_groups'
        ]

class StrengthSetSerializer(FullCleanSerializer, serializers.ModelSerializer):
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

class StrengthTrainingSerializer(RelatedToUserSerializer, FullCleanSerializer, serializers.ModelSerializer):
    sets = StrengthSetSerializer(many = True, read_only = True)

    class Meta:
        model  = StrengthTraining
        fields = [
            'id', 'user', 'date', 'sets'
        ]

"""
Cardio-related serializers
"""

class CardioExerciseSerializer(FullCleanSerializer, serializers.ModelSerializer):
    class Meta:
        model  = CardioExercise
        fields = [
            'id', 'name', 'description',
            'calories_burned_per_minute'
        ]

class CardioSetSerializer(FullCleanSerializer, serializers.ModelSerializer):
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

class CardioTrainingSerializer(RelatedToUserSerializer, FullCleanSerializer, serializers.ModelSerializer):
    sets = CardioSetSerializer(many = True, read_only = True)

    class Meta:
        model  = CardioTraining
        fields = [
            'id', 'user', 'date', 'sets'
        ]
