import logging

from django.db.models.query import QuerySet
from django.http import request
from django.http.response import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response

import ingredients.services as service

logger = logging.getLogger(__name__)


class IngredientsRestAPI(viewsets.ViewSet):
    def list(self, request: request) -> HttpResponse:
        logger.info('Метод IngredientsRestAPI list вызван')
        return Response(service.IngredientsService(request).list())

    def retrieve(self, request: request, pk: str) -> HttpResponse:
        logger.info('Метод IngredientsRestAPI retrieve вызван')
        return Response(service.IngredientsService(request, self.kwargs).retrieve())


class IngredientsAppAPI:
    def get_ingredient(self, pk: int) -> dict:
        logger.info('Метод IngredientsAppAPI get_ingredient вызван')
        return service.IngredientsService().get_ingredient(pk=pk)


class IngredientsAdminAPI:
    def get_ingredients(self) -> QuerySet:
        logger.info('Метод IngredientAdminAPI get_ingredients вызван')
        return service.IngredientsAdminService().get_ingredients()
