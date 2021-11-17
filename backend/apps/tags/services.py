import logging

from rest_framework import serializers

from utils.base_services import BaseService

from .models import Tag
from .serializers import TagSerializer

logger = logging.getLogger(__name__)


class TagsService(BaseService):
    def __init__(self):
        self.instance = Tag

    def get_all(self) -> dict:
        logger.info('Get list of tags.')
        serializer = TagSerializer(super().get_all(), many=True)
        return serializer.data

    def get_by_id(self, instance_id: int) -> dict:
        logger.info('Get tag by id.')
        serializer = TagSerializer(super().get_by_id(instance_id))
        return serializer.data
