import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import FavoritesService

logger = logging.getLogger(__name__)


class FavoritesAPI(viewsets.ViewSet):

    service = FavoritesService()

    @action(detail=True, url_path='favorite', permission_classes=[IsAuthenticated])
    def add_recipe_to_favorite(self, request: request, pk: str = None) -> HttpResponse:
        logger.info('Метод FavoritesApi add_recipe_to_favorite вызван')
        return Response(self.service.add_recipe_to_favorite(request, pk=int(pk)))

    @add_recipe_to_favorite.mapping.delete
    def delete_recipe_from_favorite(self, request, pk: str = None) -> HttpResponse:
        logger.info('Метод FavoritesApi delete_recipe_from_favorite вызван')
        self.service.delete_recipe_from_favorite(request, pk=int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def check_is_favorited(self, recipe: int, user: int) -> HttpResponse:
        logger.info('Метод FavoritesApi check_is_favorited вызван')
        return Response(self.service.check_is_favorited(recipe=recipe, user=user))

    def get_user_favorite_recipes(self, user: int) -> HttpResponse:
        logger.info('Метод FavoritesApi get_user_favorite_recipes вызван')
        return Response(self.service.get_user_favorite_recipes(user=user))
