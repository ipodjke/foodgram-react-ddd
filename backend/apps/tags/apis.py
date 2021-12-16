import logging

from django.db.models.query import QuerySet
from django.http import request
from django.http.response import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response

import tags.services as service

logger = logging.getLogger(__name__)


class TagsRestAPI(viewsets.ViewSet):
    def list(self, request: request) -> HttpResponse:
        logger.info('Метод TagsRestAPI list вызван')
        return Response(service.TagsService(request).list())

    def retrieve(self, request: request, pk: str) -> HttpResponse:
        logger.info('Метод TagsRestAPI retrieve вызван')
        return Response(service.TagsService(request, self.kwargs).retrieve())


class TagsAppAPI:
    def get_tag_by_slug(self, slug: str) -> dict:
        logger.info('Метод TagsAppAPI get_tag_by_slug вызван')
        return service.TagsService().get_tag_by_slug(slug=slug)

    def get_tag(self, pk: int) -> dict:
        logger.info('Метод TagsAppAPI get_tag вызван')
        return service.TagsService().get_tag(pk=pk)


class TagsAdminAPI:
    def get_tags(self) -> QuerySet:
        logger.info('Метод TagsAdminAPI get_tags вызван')
        return service.TagsAdminService().get_tags()
