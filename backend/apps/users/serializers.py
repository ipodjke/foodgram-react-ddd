from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

import users.services as services

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
        ) + tuple(User.REQUIRED_FIELDS) + ('password',)


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
        ) + tuple(User.REQUIRED_FIELDS) + ('is_subscribed',)

    def get_is_subscribed(self, obj):
        return services.UsersService().check_is_subscribed(context=self.context, author=obj)


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={'input_type': 'password'})
    current_password = serializers.CharField(style={'input_type': 'password'})

    def validate_new_password(self, value):
        try:
            validate_password(value, self.context['request'].user)
            return value
        except ValidationError:
            raise serializers.ValidationError(
                {'new_password': list(ValidationError.messages)}
            )

    def validate_current_password(self, value):
        if self.context['request'].user.check_password(value):
            return value

        raise serializers.ValidationError(
            django_settings.ERROR_MESSAGE.get('current_password')
        )
