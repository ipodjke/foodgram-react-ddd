import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import FavoritesService

logger = logging.getLogger(__name__)


class FavoritesAPI(viewsets.ViewSet):

    favorites_service = FavoritesService()

    @action(detail=True, url_path='favorite_new', permission_classes=[IsAuthenticated])
    def mark_favorite_recipe(self, request: request, pk: str = None) -> HttpResponse:
        return Response(self.favorites_service.add_recipe_to_favorite(request, pk=int(pk)))

    @mark_favorite_recipe.mapping.delete
    def delete_favorite_recipe(self, request, pk: str = None) -> HttpResponse:
        self.favorites_service.remove_recipe_from_favorite(request, pk=int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)
