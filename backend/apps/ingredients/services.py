import logging

from django.db.models.query import QuerySet

from utils.base_services import BaseService

from .models import Ingredient
from .serializers import IngredientSerializer
from .utils.filters import DoubleSearchBackend

logger = logging.getLogger(__name__)


class IngredientsService(BaseService):
    instance = Ingredient
    serializer_class = IngredientSerializer
    filter_backends = [DoubleSearchBackend]
    search_fields = ['^name', '$name']
    pagination_class = None

    # APP API logic
    def get_ingredient(self, pk: int) -> dict:
        logger.info('Метод IngredientsService get_ingredient вызван')
        return self.retrieve(pk=pk)


class IngredientsAdminService:
    instance = Ingredient

    def get_ingredients(self) -> QuerySet:
        logger.info('Метод IngredientsAdminService get_ingredients вызван')
        return self.instance.objects.all()
