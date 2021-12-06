import logging

from django.db.models.query import QuerySet
from django.http import request
from django.http.response import HttpResponse

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import favorites.services as service

logger = logging.getLogger(__name__)


class FavoritesRestAPI(viewsets.ViewSet):
    @action(detail=True, url_path='favorite', permission_classes=[IsAuthenticated])
    def add_recipe_to_favorite(self, request: request, pk: str) -> HttpResponse:
        logger.info('Метод FavoritesRestAPI add_recipe_to_favorite вызван')
        return Response(service.FavoritesService(request).add_recipe_to_favorite(pk=int(pk)))

    @add_recipe_to_favorite.mapping.delete
    def delete_recipe_from_favorite(self, request: request, pk: str) -> HttpResponse:
        logger.info('Метод FavoritesRestAPI delete_recipe_from_favorite вызван')
        if service.FavoritesService(request, self.kwargs).delete_recipe_from_favorite(pk=int(pk)):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class FavoritesAppAPI:
    def check_is_favorited(self, recipe: int, user: int) -> bool:
        logger.info('Метод FavoritesAppAPI check_is_favorited вызван')
        return service.FavoritesService().check_is_favorited(recipe=recipe, user=user)

    def get_user_favorite_recipes(self, user: int) -> QuerySet:
        logger.info('Метод FavoritesAppAPI get_user_favorite_recipes вызван')
        return service.FavoritesService().get_user_favorite_recipes(user=user)


class FavoritesAdminAPI:
    def get_total_number_of_additions(self, pk: int) -> int:
        logger.info('Метод FavoritesAdminAPI get_total_number_of_additions вызван')
        return service.FavoritesAdminService().get_total_number_of_additions(pk=pk)
