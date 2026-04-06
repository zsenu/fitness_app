from rest_framework                 import serializers
from django.db                      import transaction

from django.contrib.auth.models     import User
from core.models                    import UserProfile
from core.models                    import HealthLog
from core.models                    import FoodItem,       FoodLog,          FoodEntry
from core.models                    import MuscleGroup,    StrengthExercise, StrengthSet, StrengthTraining
from core.models                    import CardioExercise, CardioSet,        CardioTraining

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
        m2m_fields = [field.name for field in self.Meta.model._meta.many_to_many]

        instance = getattr(self, 'instance', None) or self.Meta.model()

        for attr, value in attrs.items():
            if attr not in m2m_fields:
                setattr(instance, attr, value)

        instance.full_clean()
        return attrs

"""
User-related serializers
"""
class UserProfileRegistrationSerializer(FullCleanSerializer, serializers.ModelSerializer):
    class Meata:
        model = UserProfile
        fields = [
            'gender', 'birth_date', 'height',
            'starting_weight', 'target_weight', 'target_date'
        ]

class RegisterSerializer(FullCleanSerializer, serializers.ModelSerializer):
    profile = UserProfileRegistrationSerializer(write_only = True)

    class Meta:
        model  = User
        fields = [
            'username', 'email', 'password', 'profile'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        profile_data = attrs.get('profile', None)

        if not profile_data:
            raise serializers.ValidationError({ 'profile': 'This field is required.' })
        
        profile_serializer = UserProfileRegistrationSerializer(data = profile_data)
        profile_serializer.is_valid(raise_exception = True)
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')

        user = User.objects.create_user(
            username = validated_data['username'],
            email    = validated_data['email'],
            password = validated_data['password']
        )

        UserProfile.objects.create(user = user, **profile_data)

        return user

class UserProfileSerializer(FullCleanSerializer, serializers.ModelSerializer):
    user_id        =          serializers.IntegerField(source = 'user.id',       read_only = True)
    username       =             serializers.CharField(source = 'user.username', read_only = True)
    email          =             serializers.CharField(source = 'user.email',    read_only = True)
    current_weight = serializers.SerializerMethodField()

    def get_current_weight(self, obj):
        latest_log = obj.user.healthlog_set.filter(bodyweight__isnull = False).first()
        return latest_log.bodyweight if latest_log else obj.starting_weight

    class Meta:
        model  = UserProfile
        fields = [
            'user_id', 'username', 'email',
            'gender', 'birth_date', 'height',
            'starting_weight', 'current_weight', 'target_weight', 'target_date'
        ]
        read_only_fields = [
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

class FoodEntrySerializer(FullCleanSerializer, serializers.ModelSerializer):
    parent_log_id = serializers.PrimaryKeyRelatedField(
        queryset = FoodLog.objects.all(),
        required = False
    )
    food_item = FoodItemSerializer(read_only = True)
    food_item_id = serializers.PrimaryKeyRelatedField(
        queryset = FoodItem.objects.all(),
        source = 'food_item',
        write_only = True
    )

    class Meta:
        model  = FoodEntry
        fields = [
            'id',
            'parent_log', 'meal_type',
            'food_item', 'food_item_id',
            'quantity', 'description'
        ]

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
class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = [
            'id', 'name'
        ]

class StrengthExerciseSerializer(FullCleanSerializer, serializers.ModelSerializer):
    target_muscle_groups = MuscleGroupSerializer(many = True, read_only = True)
    target_muscle_group_ids = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = MuscleGroup.objects.all(),
        source = 'target_muscle_groups',
        write_only = True
    )

    class Meta:
        model  = StrengthExercise
        fields = [
            'id', 'name', 'description',
            'target_muscle_groups', 'target_muscle_group_ids'
        ]

    def create(self, validated_data):
        muscle_groups = validated_data.pop('target_muscle_groups', [])
        exercise = StrengthExercise.objects.create(**validated_data)
        exercise.target_muscle_groups.set(muscle_groups)
        return exercise

class StrengthSetSerializer(FullCleanSerializer, serializers.ModelSerializer):
    parent_log_id = serializers.PrimaryKeyRelatedField(
        queryset = StrengthTraining.objects.all(),
        required = False
    )
    exercise = StrengthExerciseSerializer(read_only = True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset = StrengthExercise.objects.all(),
        source = 'exercise',
        write_only = True
    )

    class Meta:
        model  = StrengthSet
        fields = [
            'id',
            'parent_log',
            'exercise_id', 'exercise',
            'weight', 'reps', 'description'
        ]

class StrengthTrainingSerializer(RelatedToUserSerializer, FullCleanSerializer, serializers.ModelSerializer):
    sets = StrengthSetSerializer(many = True, read_only = True, source = 'session_sets')

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
            'calories_per_minute'
        ]

class CardioSetSerializer(FullCleanSerializer, serializers.ModelSerializer):
    parent_log_id = serializers.PrimaryKeyRelatedField(
        queryset = CardioTraining.objects.all(),
        required = False
    )
    exercise = CardioExerciseSerializer(read_only = True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset = CardioExercise.objects.all(),
        source = 'exercise',
        write_only = True
    )

    class Meta:
        model  = CardioSet
        fields = [
            'id',
            'parent_log',
            'exercise_id', 'exercise',
            'duration', 'description'
        ]

class CardioTrainingSerializer(RelatedToUserSerializer, FullCleanSerializer, serializers.ModelSerializer):
    sets = CardioSetSerializer(many = True, read_only = True, source = 'session_sets')

    class Meta:
        model  = CardioTraining
        fields = [
            'id', 'user', 'date', 'sets'
        ]
