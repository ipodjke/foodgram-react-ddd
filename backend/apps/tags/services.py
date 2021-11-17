import logging

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
