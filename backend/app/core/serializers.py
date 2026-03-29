from datetime                   import date
from rest_framework             import serializers

from django.contrib.auth.models import User
from .models                    import UserProfile

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
