import logging
from typing import Union

from django.conf import settings
from django.db.models.query import QuerySet
from django.http.response import Http404

from rest_framework.exceptions import ValidationError

import favorites.interfaces as interface
from utils.base_services import BaseService

from .models import Favorites
from .serializers import FavoritesSerializer


class FavoritesService(BaseService):

    instance = Favorites
    serializer_class = FavoritesSerializer
    lookup_field = 'recipe'
    lookup_url_kwarg = 'pk'
    include_to_lookup = {'user': 'self.request.user.id'}
    filter_backends = []
    pagination_class = None
    logger = logging.getLogger(__name__)

    # REST API logic
    def add_recipe_to_favorite(self, pk: int) -> dict:
        self.logger.info('Метод FavoritesService add_recipe_to_favorite вызван')
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
        self.logger.info('Метод FavoritesService delete_recipe_from_favorite вызван')
        self._validate_delete_request(user=self.request.user.id, recipe=pk)
        self.get_object().delete()
        return True

    # APP API logic
    def check_is_favorited(self, recipe: int, user: int) -> bool:
        self.logger.info('Метод FavoritesService check_is_favorited вызван')
        context = {'user': user, 'recipe': recipe}
        return self.check_is_in(context)

    def get_user_favorite_recipes(self, user: int) -> QuerySet:
        self.logger.info('Метод FavoritesService get_user_favorite_recipes вызван')
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
