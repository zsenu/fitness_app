from rest_framework         import serializers
from django.contrib.auth    import get_user_model, password_validation
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()

from core.models            import HealthLog
from core.models            import FoodItem,       FoodLog,          FoodEntry
from core.models            import MuscleGroup,    StrengthExercise, StrengthSet, StrengthTraining
from core.models            import CardioExercise, CardioSet,        CardioTraining

"""
Abstract serializers to apply certain behaviors
"""
class RelatedToUserMixin(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())

    class Meta:
        abstract = True

class FullValidationMixin(serializers.ModelSerializer):
    class Meta:
        abstract = True

    def inject_context_fields(self, attrs):
        context_fields = getattr(self.Meta, 'context_fields', [])
        for field_name in context_fields:
            if field_name in self.context:
                attrs[field_name] = self.context[field_name]
        return attrs
    
    def setattr_without_m2m(self, instance, attrs):
        m2m_fields = [field.name for field in self.Meta.model._meta.many_to_many]

        for attr, value in attrs.items():
            if attr not in m2m_fields:
                setattr(instance, attr, value)

    def synchronize_attrs_with_instance(self, instance, attrs):
        m2m_fields = [field.name for field in self.Meta.model._meta.many_to_many]
        for attr in attrs.keys():
            if attr not in m2m_fields:
                attrs[attr] = getattr(instance, attr)

    def validate(self, attrs):
        attrs = self.inject_context_fields(attrs)

        instance = getattr(self, 'instance', None) or self.Meta.model()

        self.setattr_without_m2m(instance, attrs)

        try:
            instance.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        self.synchronize_attrs_with_instance(instance, attrs)

        return attrs

"""
User-related serializers
"""
class UserSerializer(FullValidationMixin):
    current_weight = serializers.SerializerMethodField()
    bmr            = serializers.SerializerMethodField()
    tdee           = serializers.SerializerMethodField()

    def get_current_weight(self, obj):
        latest_log = obj.healthlog_set.filter(bodyweight__isnull = False).first()
        return latest_log.bodyweight if latest_log else obj.starting_weight
    
    def get_bmr(self, obj):
        return obj.bmr
    
    def get_tdee(self, obj):
        return obj.tdee

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'gender', 'birth_date', 'height',
            'starting_weight', 'current_weight', 'activity_level',
            'target_weight', 'target_date', 'target_calories',
            'bmr', 'tdee'
        ]
        read_only_fields = [
            'id', 'username', 'email',
            'gender', 'birth_date', 'height', 'starting_weight',
            'bmr', 'tdee'
        ]

class RegisterSerializer(FullValidationMixin):
    password  = serializers.CharField(write_only = True, required = True)
    password2 = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'gender', 'birth_date', 'height',
            'starting_weight','activity_level',
            'target_weight', 'target_date', 'target_calories'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({ 'password': 'Password fields didn\'t match.' })
        
        try:
            password_validation.validate_password(attrs['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({ 'password': e.messages })
        
        temp_attrs = attrs.copy()
        temp_attrs.pop('password2')
        temp_user = User(**temp_attrs)

        try:
            temp_user.full_clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        
        return attrs
    
    def is_valid(self, *, raise_exception = False):
        super().is_valid(raise_exception = False)

        temp_attrs = self.initial_data.copy()
        temp_attrs.pop('password2', None)

        temp_user = User()
        for field, value in temp_attrs.items():
            setattr(temp_user, field, value)

        try:
            temp_user.full_clean()
        except DjangoValidationError as e:
            if not hasattr(self, '_errors'):
                self._errors = {}
            self._errors.update(e.message_dict)

        if self._errors and raise_exception:
            raise serializers.ValidationError(self._errors)

        return not bool(self._errors)

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

"""
Health-related serializers
"""
class HealthLogSerializer(RelatedToUserMixin, FullValidationMixin):
    class Meta:
        model  = HealthLog
        fields = [
            'id', 'user', 'date',
            'bodyweight', 'hours_slept', 'liquid_consumed'
        ]

"""
Food-related serializers
"""
class FoodItemSerializer(FullValidationMixin):
    class Meta:
        model  = FoodItem
        fields = [
            'id', 'name', 'description',
            'calories', 'fat', 'carbohydrates', 'protein'
        ]

class FoodEntrySerializer(FullValidationMixin):
    parent_log = serializers.PrimaryKeyRelatedField(read_only = True)
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
        context_fields = ['parent_log']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except DjangoValidationError as e:
            raise serializers.ValidationError({ 'non_field_errors': ['An entry for this meal type already exists in the log.'] })

class FoodLogSerializer(RelatedToUserMixin, FullValidationMixin):
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

class StrengthExerciseSerializer(FullValidationMixin):
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

class StrengthSetSerializer(FullValidationMixin):
    parent_log = serializers.PrimaryKeyRelatedField(read_only = True)
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
        context_fields = ['parent_log']

class StrengthTrainingSerializer(RelatedToUserMixin, FullValidationMixin):
    sets = StrengthSetSerializer(many = True, read_only = True, source = 'session_sets')

    class Meta:
        model  = StrengthTraining
        fields = [
            'id', 'user', 'date', 'sets'
        ]

"""
Cardio-related serializers
"""
class CardioExerciseSerializer(FullValidationMixin):
    class Meta:
        model  = CardioExercise
        fields = [
            'id', 'name', 'description',
            'calories_per_minute'
        ]

class CardioSetSerializer(FullValidationMixin):
    parent_log = serializers.PrimaryKeyRelatedField(read_only = True)
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
        context_fields = ['parent_log']

class CardioTrainingSerializer(RelatedToUserMixin, FullValidationMixin):
    sets = CardioSetSerializer(many = True, read_only = True, source = 'session_sets')

    class Meta:
        model  = CardioTraining
        fields = [
            'id', 'user', 'date', 'sets'
        ]
