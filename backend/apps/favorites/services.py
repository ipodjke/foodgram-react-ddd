import logging
from typing import Union

from django.conf import settings
from django.db.models.query import QuerySet
from django.http.response import Http404
from rest_framework.exceptions import ValidationError

import favorites.interfaces as interface
from .models import Favorite
from .serializers import FavoritesSerializer
from utils.base_services import BaseService

logger = logging.getLogger(__name__)


class FavoritesService(BaseService):

    instance = Favorite
    serializer_class = FavoritesSerializer
    lookup_field = 'recipe'
    lookup_url_kwarg = 'pk'
    include_to_lookup = {'user': 'self.request.user.id'}
    filter_backends = []
    pagination_class = None

    # REST API logic
    def add_recipe_to_favorite(self, pk: int) -> dict:
        logger.info('Метод FavoritesService add_recipe_to_favorite вызван')
        # recipe ловим Http404 exception, не возможно добавить не существующий рецепт.
        recipe = interface.RecipesInrerface().get_recipe_with_shot_serializer(request=self.request,
                                                                              pk=pk)
        data = {
            'user': self.request.user.id,
            'recipe': pk
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return recipe # noqa

    def delete_recipe_from_favorite(self, pk: int) -> bool:
        logger.info('Метод FavoritesService delete_recipe_from_favorite вызван')
        self._validate_delete_request(user=self.request.user.id, recipe=pk)
        self.get_object().delete()
        return True

    # APP API logic
    def check_is_favorited(self, recipe: int, user: int) -> bool:
        logger.info('Метод FavoritesService check_is_favorited вызван')
        context = {'user': user, 'recipe': recipe}
        return self.check_is_in(context)

    def get_user_favorite_recipes(self, user: int) -> QuerySet:
        logger.info('Метод FavoritesService get_user_favorite_recipes вызван')
        return self.get_queryset().filter(user=user)

    # local functions
    def _validate_delete_request(self, user: int, recipe: int) -> Union[ValidationError,
                                                                        Http404,
                                                                        None]:
        interface.RecipesInrerface().get_recipe_with_shot_serializer(request=self.request,
                                                                     pk=recipe)
        if not self.instance.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('not_in_favorited')}
            )


class FavoritesAdminService:
    instance = Favorite

    def get_total_number_of_additions(self, pk: int) -> QuerySet:
        logger.info('Метод FavoritesAdminService get_total_number_of_additions вызван')
        return self.instance.objects.filter(recipe=pk).count()

    # interface logic
    # Recipes
    def get_recipes(self) -> QuerySet:
        logger.info('Метод FavoritesAdminService get_recipes вызван')
        return interface.RecipesAdminInterface().get_recipes()

    def get_recipe(self, pk: int) -> QuerySet:
        logger.info('Метод FavoritesAdminService get_recipe вызван')
        return interface.RecipesAdminInterface().get_recipe(pk=pk)

    # Users
    def get_users(self) -> QuerySet:
        logger.info('Метод FavoritesAdminService get_users вызван')
        return interface.UsersAdminInterface().get_users()

    def get_user(self, pk: int) -> QuerySet:
        logger.info('Метод FavoritesAdminService get_user вызван')
        return interface.UsersAdminInterface().get_user(pk=pk)
