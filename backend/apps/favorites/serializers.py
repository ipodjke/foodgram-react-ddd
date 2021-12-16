from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Favorite


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

    def validate_recipe(self, value):
        if self.Meta.model.objects.filter(user=self.initial_data.get('user'),
                                          recipe=self.initial_data.get('recipe')).exists():
            raise ValidationError(settings.ERROR_MESSAGE.get('alredy_favorited'))
        return value
