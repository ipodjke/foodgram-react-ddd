import logging

from django.http import request
from django.http.response import FileResponse, HttpResponse

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import ShoppingCartService

logger = logging.getLogger(__name__)


class ShoppingCartAPI(viewsets.ViewSet):

    service = ShoppingCartService()

    @action(detail=True, url_path='shopping_cart', permission_classes=[IsAuthenticated])
    def add_to_shopping_cart(self, request: request, pk: str = None) -> HttpResponse:
        logger.info('Метод ShoppingCartAPI add_to_shopping_cart вызван')
        return Response(self.service.add_to_shopping_cart(request, pk=int(pk)))

    @add_to_shopping_cart.mapping.delete
    def delete_from_shopping_cart(self, request: request, pk: str = None) -> HttpResponse:
        logger.info('Метод ShoppingCartAPI delete_from_shopping_cart вызван')
        self.service.delete_from_shopping_cart(request, pk=int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, url_path='download_shopping_cart', permission_classes=[IsAuthenticated]) # noqa
    def download_shopping_cart(self, request: request) -> FileResponse:
        logger.info('Метод ShoppingCartAPI download_shopping_cart вызван')
        file_response_params = self.service.download_shopping_cart(request=request)
        file = file_response_params.pop('file')
        return FileResponse(file, **file_response_params)

    def check_is_in_shopping_cart(self, recipe: int, user: int) -> HttpResponse:
        logger.info('Метод ShoppingCartAPI check_is_in_shopping_cart вызван')
        return Response(self.service.check_is_in_shopping_cart(recipe=recipe, user=user))

    def get_user_shopping_cart(self, user: int) -> HttpResponse:
        logger.info('Метод ShoppingCartAPI get_user_shopping_cart вызван')
        return Response(self.service.get_user_shopping_cart(user=user))
