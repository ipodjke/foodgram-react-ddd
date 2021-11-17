from rest_framework import serializers


class UserIsFollowing():

    def __call__(self, serializer_field, *args, **kwargs):
        if serializer_field.get('is_subscribed') is True:
            raise serializers.ValidationError(
                'Вы уже подписаны'
            )
