import logging

from django.db.models.query import QuerySet

from .models import Tag
from .serializers import TagSerializer
from utils.base_services import BaseService

logger = logging.getLogger(__name__)


class TagsService(BaseService):
    instance = Tag
    serializer_class = TagSerializer
    filter_backends = []
    pagination_class = None

    # APP API logic
    def get_tag_by_slug(self, slug: str) -> dict:
        logger.info('Метод TagsService get_tag_by_slug вызван')
        context = {'slug': slug}
        serializer = self.get_serializer(self.get_object(context=context))
        return serializer.data

    def get_tag(self, pk: int) -> dict:
        logger.info('Метод TagsService get_tag вызван')
        return self.retrieve(pk=pk)


class TagsAdminService:
    instance = Tag

    def get_tags(self) -> QuerySet:
        logger.info('Метод TagsAdminService get_tags вызван')
        return self.instance.objects.all()
