import logging

from django.conf import settings
from django.http import request

from rest_framework.exceptions import ValidationError

import favorites.interfaces as interface
from utils.base_services import BaseService

from .models import Favorites

logger = logging.getLogger(__name__)


class FavoritesService(BaseService):
    def __init__(self):
        self.instance = Favorites

    def add_recipe_to_favorite(self, request: request, pk: int = None) -> dict:
        logger.info('Метод FavoritesService add_recipe_to_favorite вызван')
        if self.instance.objects.filter(user=request.user.id, recipe=pk).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('alredy_favorited')}
            )
        self.instance.objects.create(user=request.user.id, recipe=pk)
        return interface.RecipesInrerface().get_short_recipe(pk=pk)

    def delete_recipe_from_favorite(self, request: request, pk: int = None) -> bool:
        logger.info('Метод FavoritesService delete_recipe_from_favorite вызван')
        if not self.instance.objects.filter(user=request.user.id, recipe=pk).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('not_in_favorited')}
            )
        self.instance.objects.get(user=request.user.id, recipe=pk).delete()
        return True

    def check_is_favorited(self, recipe: int, user: int) -> bool:
        logger.info('Метод FavoritesService check_is_favorited вызван')
        return self.instance.objects.filter(user=user, recipe=recipe).exists()

    def get_user_favorite_recipes(self, user: int) -> dict:
        logger.info('Метод FavoritesService get_user_favorite_recipes вызван')
        return self.instance.objects.filter(user=user)
