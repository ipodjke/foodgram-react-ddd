from rest_framework import serializers

import subscriptions.services as service


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
        limit = self.context.get('limit')
        if limit is None:
            return service.SubscriptionsService().get_recipes(author=obj.get('id'))
        return service.SubscriptionsService().get_recipes(author=obj.get('id'))[:int(limit)]

    def get_recipes_count(self, obj):
        return service.SubscriptionsService().get_count_recipes(author=obj.get('id')).get('count')
