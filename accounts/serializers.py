from abc import ABC

from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(
        max_length=60,
        min_length=6,
        write_only=True,
        style={'input_type': 'password'},
        label='Password'
    )
    confirm_password = serializers.CharField(
        max_length=60,
        min_length=6,
        write_only=True,
        style={'input_type': 'password'},
        label='Confirm password'
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password',
                  'first_name', 'last_name', 'birth_date', )

    def validate(self, attrs):
        password = attrs.get('password', '')
        confirm_password = attrs.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords don't match")
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(TokenSerializer, self).validate(attrs)
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not user.is_verified:
                raise serializers.ValidationError("Confirm your email address")
            else:
                data.update({'time_access': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']})
                data.update({'time_refresh': settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']})
                return data
