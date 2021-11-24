import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response

from .services import IngredientsService

logger = logging.getLogger(__name__)


class IngredientsRestAPI(viewsets.ViewSet):
    service = IngredientsService

    def list(self, request: request) -> HttpResponse:
        logger.info('Метод IngredientsRestAPI list вызван')
        return Response(self.service(request).list())

    def retrieve(self, request: request, pk: str) -> HttpResponse:
        logger.info('Метод IngredientsRestAPI retrieve вызван')
        return Response(self.service(request, self.kwargs).retrieve())


class IngredientsAppAPI:
    service = IngredientsService

    def get_ingredient(self, pk: int) -> dict:
        logger.info('Метод IngredientsAppAPI get_ingredient вызван')
        return self.service().get_ingredient(pk=pk)
