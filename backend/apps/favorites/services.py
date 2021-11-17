import logging
from collections import OrderedDict
from re import A

from django.conf import settings
from django.http import request

import subscriptions.services as service
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from recipes.interfaces import UsersInterface
from utils.base_services import BaseService

from .interfaces import RecipesInrerface, UserInterface
from .models import Favorites
from .serializers import SubscriptionsSerializer

logger = logging.getLogger(__name__)


class FavoritesService(BaseService):
    def __init__(self):
        self.instance = Favorites

    def add_recipe_to_favorite(self, request: request, pk: int = None) -> dict:
        if self.instance.objects.filter(user=request.user.id, recipe=pk).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('alredy_favorited')}
            )
        self.instance.objects.create(user=request.user.id, recipe=pk)
        return RecipesInrerface().get_short_recipe(pk=pk)

    def remove_recipe_from_favorite(self, request: request, pk: int = None) -> bool:
        if not self.instance.objects.filter(user=request.user.id, recipe=pk).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('not_in_favorited')}
            )
        self.instance.objects.get(user=request.user.id, recipe=pk).delete()
        return True
