import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response

from .services import TagsService

logger = logging.getLogger(__name__)


class TagsRestAPI(viewsets.ViewSet):
    service = TagsService

    def list(self, request: request) -> HttpResponse:
        logger.info('Метод TagsRestAPI list вызван')
        return Response(self.service(request).list())

    def retrieve(self, request: request, pk: str) -> HttpResponse:
        logger.info('Метод TagsRestAPI retrieve вызван')
        return Response(self.service(request, self.kwargs).retrieve())


class TagsAppAPI:
    service = TagsService

    def get_tag_by_slug(self, slug: str) -> dict:
        logger.info('Метод TagsAppAPI get_tag_by_slug вызван')
        return self.service().get_tag_by_slug(slug=slug)

    def get_tag(self, pk: int) -> dict:
        logger.info('Метод TagsAppAPI get_tag вызван')
        return self.service().get_tag(pk=pk)
