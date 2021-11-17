import logging

from django.http import request

from rest_framework import viewsets
from rest_framework.response import Response

from .services import IngredientsService

logger = logging.getLogger(__name__)


class IngredientsAPI(viewsets.ViewSet):

    ingredient_service = IngredientsService()

    def list(self, request: object) -> dict:
        logger.info('Метод IngredientsAPI list вызван')
        return Response(self.ingredient_service.get_all())

    def retrieve(self, request: request = None, pk: int = None) -> dict:
        logger.info('Метод IngredientsAPI retrieve вызван')
        return Response(self.ingredient_service.get_by_id(instance_id=pk))
