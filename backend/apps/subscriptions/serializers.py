from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

import subscriptions.services as service
from djoser.conf import settings
from djoser.serializers import \
    UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

from recipes.models import Recipe
from utils.generalizing_functions import check_the_occurrence

User = get_user_model()


class CreateUserSerializer(DjoserUserCreateSerializer):
    class Meta:
        model = User
        fields = (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
        ) + tuple(User.REQUIRED_FIELDS) + ('password',)


class UserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
        ) + tuple(User.REQUIRED_FIELDS) + ('is_subscribed',)

    def get_is_subscribed(self, obj):
        return check_the_occurrence(obj, 'subscriptions', self)


class LimitedListRecipieSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        limit = self.context.get('request').query_params.get('recipes_limit')

        if limit is None:
            return super().to_representation(data)

        return super().to_representation(data.all()[:int(limit)])


class SubscribtionsRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = LimitedListRecipieSerializer
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribtionsUserSerializer(UserSerializer):
    recipes = SubscribtionsRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    is_subscribed = serializers.BooleanField()
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        print(self.context.get('limit'))
        limit = self.context.get('limit')
        if limit is None:
            return service.SubscriptionsService().get_recipes(author=obj.get('id'))
        return service.SubscriptionsService().get_recipes(author=obj.get('id'))[:int(limit)]

    def get_recipes_count(self, obj):
        return service.SubscriptionsService().get_count_recipes(author=obj.get('id')).get('count')
