import logging

from django.http import request

from rest_framework import viewsets
from rest_framework.response import Response

from .services import TagsService

logger = logging.getLogger(__name__)


class TagsAPI(viewsets.ViewSet):

    tag_service = TagsService()

    def list(self, request: object) -> dict:
        logger.info('Метод TagsAPI list вызван')
        return Response(self.tag_service.get_all())

    def retrieve(self, request: request = None, pk: int = None) -> dict:
        logger.info('Метод TagsAPI retrieve вызван')
        return Response(self.tag_service.get_by_id(instance_id=pk))
