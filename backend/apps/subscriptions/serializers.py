from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import subscriptions.services as service
from .models import Subscription


class SubscriptionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    is_subscribed = serializers.BooleanField()
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    def get_recipes(self, obj):
        limit = self.context.get('request').query_params.get('recipes_limit')
        if limit is None:
            return service.SubscriptionsService().get_author_recipes(author=obj.get('id'))
        return service.SubscriptionsService().get_author_recipes(author=obj.get('id'))[:int(limit)]

    def get_recipes_count(self, obj):
        return service.SubscriptionsService().get_count_author_recipes(author=obj.get('id'))

    def validate(self, attrs):
        if self.context.get('request').user.id == attrs.get('id'):
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('self_subscription')}
            )

        if Subscription.objects.filter(follower=self.context.get('request').user.id,
                                       author=attrs.get('id')).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('alredy_subscribe')}
            )

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['is_subscribed'] = True
        return Subscription.objects.create(follower=self.context.get('request').user.id,
                                           author=validated_data.get('id'))
