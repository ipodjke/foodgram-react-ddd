import logging

from utils.base_services import BaseService

from .models import Tag
from .serializers import TagSerializer


class TagsService(BaseService):
    instance = Tag
    serializer_class = TagSerializer
    filter_backends = []
    pagination_class = None
    logger = logging.getLogger(__name__)

    # APP API logic
    def get_tag_by_slug(self, slug: str) -> dict:
        self.logger.info('Метод TagsService get_tag_by_slug вызван')
        context = {'slug': slug}
        serializer = self.get_serializer(self.get_object(context=context))
        return serializer.data

    def get_tag(self, pk: int) -> dict:
        self.logger.info('Метод TagsService get_tag вызван')
        return self.retrieve(pk=pk)
