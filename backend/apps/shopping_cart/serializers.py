from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import ShoppingCart


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'

    def validate_recipe(self, value):
        if self.Meta.model.objects.filter(user=self.initial_data.get('user'),
                                          recipe=self.initial_data.get('recipe')).exists():
            raise ValidationError(settings.ERROR_MESSAGE.get('alredy_in_cart'))
        return value
