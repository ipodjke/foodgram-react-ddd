import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import RecipesService

logger = logging.getLogger(__name__)


class RecipesAPI(viewsets.ViewSet):

    recipes_service = RecipesService()

    def list(self, request: request) -> HttpResponse:
        return Response(self.recipes_service.get_pagination_list(request))

    def create(self, request: request) -> HttpResponse:
        return Response(self.recipes_service.create_recipe(request))

    def retrieve(self, request: request = None, pk: int = None) -> HttpResponse:
        logger.info('Метод TagsAPI retrieve вызван')
        return Response(self.recipes_service.get_by_id(pk=pk))

    def destroy(self, request: request, pk: int = None) -> HttpResponse:
        self.recipes_service.delete(pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request: request, pk: int = None, **kwargs) -> HttpResponse:
        kwargs['partial'] = True
        return self.update(request=request, pk=pk, **kwargs)

    def update(self, request: request, pk: int = None, **kwargs) -> HttpResponse:
        return Response(self.recipes_service.update(request=request, pk=pk, **kwargs))

    def get_author_recipes(self, author: int = None) -> HttpResponse:
        return Response(self.recipes_service.get_short_recipe_list(author=author))

    def get_count_author_recipes(self, author: int = None) -> HttpResponse:
        return Response(self.recipes_service.get_count_author_recipes(author=author))

    def get_short_recipe(self, pk: str = None) -> HttpResponse:
        return Response(self.recipes_service.get_short_recipe(pk=int(pk)))
