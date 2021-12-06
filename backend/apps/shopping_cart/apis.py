import logging

from django.db.models.query import QuerySet
from django.http import request
from django.http.response import FileResponse, HttpResponse

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import shopping_cart.services as service

logger = logging.getLogger(__name__)


class ShoppingCartRestAPI(viewsets.ViewSet):
    @action(detail=True, url_path='shopping_cart', permission_classes=[IsAuthenticated])
    def add_to_shopping_cart(self, request: request, pk: str) -> HttpResponse:
        logger.info('Метод ShoppingCartRestAPI add_to_shopping_cart вызван')
        return Response(service.ShoppingCartService(request).add_to_shopping_cart(pk=int(pk)))

    @add_to_shopping_cart.mapping.delete
    def delete_from_shopping_cart(self, request: request, pk: str) -> HttpResponse:
        logger.info('Метод ShoppingCartRestAPI delete_from_shopping_cart вызван')
        if service.ShoppingCartService(request, self.kwargs).delete_from_shopping_cart(pk=int(pk)):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @action(detail=False, url_path='download_shopping_cart', permission_classes=[IsAuthenticated]) # noqa
    def download_shopping_cart(self, request: request) -> FileResponse:
        logger.info('Метод ShoppingCartRestAPI download_shopping_cart вызван')
        file_response_params = service.ShoppingCartService(request).download_shopping_cart()
        file = file_response_params.pop('file')
        return FileResponse(file, **file_response_params)


class ShoppingCartAppAPI:
    def check_is_in_shopping_cart(self, recipe: int, user: int) -> dict:
        logger.info('Метод ShoppingCartAppAPI check_is_in_shopping_cart вызван')
        return service.ShoppingCartService().check_is_in_shopping_cart(recipe=recipe, user=user)

    def get_user_shopping_cart(self, user: int) -> QuerySet:
        logger.info('Метод ShoppingCartAppAPI get_user_shopping_cart вызван')
        return service.ShoppingCartService().get_user_shopping_cart(user=user)
