import logging

from django.shortcuts import get_object_or_404

from rest_framework import serializers

from utils.base_services import BaseService

from .models import Tag
from .serializers import TagSerializer

logger = logging.getLogger(__name__)


class TagsService(BaseService):
    def __init__(self):
        self.instance = Tag

    def get_all(self) -> dict:
        logger.info('Метод TagsService get_all вызван')
        serializer = TagSerializer(super().get_all(), many=True)
        return serializer.data

    def get_by_id(self, pk: int) -> dict:
        logger.info('Метод TagsService get_by_id вызван')
        serializer = TagSerializer(super().get_by_id(pk))
        return serializer.data

    def get_tag_by_slug(self, slug: str) -> dict:
        serializer = TagSerializer(get_object_or_404(self.instance, slug=slug))
        return serializer.data
