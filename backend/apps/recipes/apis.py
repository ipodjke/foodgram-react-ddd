import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .services import RecipesService

logger = logging.getLogger(__name__)


class RecipesAPI(viewsets.ViewSet):

    service = RecipesService()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request: request) -> HttpResponse:
        logger.info('Метод RecipesAPI list вызван')
        return Response(self.service.get_pagination_list(request=request))

    def create(self, request: request) -> HttpResponse:
        logger.info('Метод RecipesAPI create вызван')
        return Response(self.service.create_recipe(request=request))

    def retrieve(self, request: request = None, pk: int = None) -> HttpResponse:
        logger.info('Метод RecipesAPI retrieve вызван')
        return Response(self.service.get_by_id(request=request, pk=pk))

    def destroy(self, request: request, pk: int = None) -> HttpResponse:
        logger.info('Метод RecipesAPI destroy вызван')
        self.service.delete(request=request, pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request: request, pk: int = None, **kwargs) -> HttpResponse:
        logger.info('Метод RecipesAPI partial_update вызван')
        kwargs['partial'] = True
        return self.update(request=request, pk=pk, **kwargs)

    def update(self, request: request, pk: int = None, **kwargs) -> HttpResponse:
        logger.info('Метод RecipesAPI update вызван')
        return Response(self.service.update(request=request, pk=pk, **kwargs))

    def get_author_recipes(self, author: int = None) -> HttpResponse:
        logger.info('Метод RecipesAPI get_author_recipes вызван')
        return Response(self.service.get_short_recipe_list(author=author))

    def get_count_author_recipes(self, author: int = None) -> HttpResponse:
        logger.info('Метод RecipesAPI get_count_author_recipes вызван')
        return Response(self.service.get_count_author_recipes(author=author))

    def get_short_recipe(self, pk: str = None) -> HttpResponse:
        logger.info('Метод RecipesAPI get_short_recipe вызван')
        return Response(self.service.get_short_recipe(pk=int(pk)))
