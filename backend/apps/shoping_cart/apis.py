import logging
import re

from django.http import request
from django.http.response import FileResponse, HttpResponse

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import ShopingCartService

logger = logging.getLogger(__name__)


class ShopingCartAPI(viewsets.ViewSet):

    shoping_cart_service = ShopingCartService()

    @action(detail=True, url_path='shoping_cart_new', permission_classes=[IsAuthenticated])
    def add_to_shoping_cart(self, request: request, pk: str = None) -> HttpResponse:
        return Response(self.shoping_cart_service.add_to_shoping_cart(request, pk=int(pk)))

    @add_to_shoping_cart.mapping.delete
    def delete_from_shoping_cart(self, request: request, pk: str = None) -> HttpResponse:
        self.shoping_cart_service.delete_from_shoping_cart(request, pk=int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, url_path='download_shoping_cart_new', permission_classes=[IsAuthenticated])
    def download_shoping_cart(self, request: request) -> FileResponse:
        file_response_params = self.shoping_cart_service.download_shoping_cart(request=request)
        file = file_response_params.pop('file')
        return FileResponse(file, **file_response_params)
        # return Response(status=status.HTTP_204_NO_CONTENT)
