import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response

from .services import IngredientsService

logger = logging.getLogger(__name__)


class IngredientsAPI(viewsets.ViewSet):

    service = IngredientsService()

    def list(self, request: object) -> HttpResponse:
        logger.info('Метод IngredientsAPI list вызван')
        return Response(self.service.get_all(request=request))

    def retrieve(self, request: request = None, pk: int = None) -> HttpResponse:
        logger.info('Метод IngredientsAPI retrieve вызван')
        return Response(self.service.get_by_id(instance_id=pk))
