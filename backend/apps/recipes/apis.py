import logging
from typing import Union

from django.db.models.query import QuerySet
from django.http import request
from django.http.response import HttpResponse
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

import recipes.services as service

logger = logging.getLogger(__name__)


class RecipesRestAPI(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request: request) -> HttpResponse:
        logger.info('Метод RecipesRestAPI list вызван')
        return Response(service.RecipesService(request).list())

    def create(self, request: request) -> HttpResponse:
        logger.info('Метод RecipesRestAPI create вызван')
        return Response(service.RecipesService(request, action=self.action).create())

    def retrieve(self, request: request, pk: str) -> HttpResponse:
        logger.info('Метод RecipesRestAPI retrieve вызван')
        return Response(service.RecipesService(request, self.kwargs).retrieve())

    def destroy(self, request: request, pk: str) -> HttpResponse:
        logger.info('Метод RecipesRestAPI destroy вызван')
        if service.RecipesService(request, self.kwargs).destroy():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def partial_update(self, request: request, pk: int, **kwargs) -> HttpResponse:
        logger.info('Метод RecipesRestAPI partial_update вызван')
        kwargs['partial'] = True
        return Response(service.RecipesService(request, self.kwargs, self.action).update(pk=pk, **kwargs)) # noqa

    def update(self, request: request, pk: int, **kwargs) -> HttpResponse:
        logger.info('Метод RecipesRestAPI update вызван')
        return Response(service.RecipesService(request, self.kwargs, self.action).update(pk=pk, **kwargs)) # noqa


class RecipesAppAPI:
    def get_author_recipes(self, author: int) -> QuerySet:
        logger.info('Метод RecipesRestAPI get_author_recipes вызван')
        return service.RecipesService(action='short_serializer').get_recipes_with_short_serializer(author=author) # noqa

    def get_count_author_recipes(self, author: int) -> int:
        logger.info('Метод RecipesRestAPI get_count_author_recipes вызван')
        return service.RecipesService().get_count_author_recipes(author=author)

    def get_recipe_with_shot_serializer(self, request: request, pk: Union[str, int]) -> dict: # noqa
        logger.info('Метод RecipesRestAPI get_short_recipe вызван')
        return service.RecipesService(request=request,
                                      action='short_serializer').get_recipe_with_shot_serializer(pk=int(pk)) # noqa

    def get_recipe(self, request: request, pk: int) -> dict:
        logger.info('Метод RecipesRestAPI get_recipe вызван')
        return service.RecipesService(request).get_recipe(pk=pk)


class RecipesAdminAPI:
    def get_recipes(self) -> QuerySet:
        logger.info('Метод RecipesAdminAPI get_recipes вызван')
        return service.RecipesAdminService().get_recipes()

    def get_recipe(self, pk: int) -> QuerySet:
        logger.info('Метод RecipesAdminAPI get_recipe вызван')
        return service.RecipesAdminService().get_recipe(pk=pk)
