import logging

from utils.base_services import BaseService

from .models import Ingredient
from .serializers import IngredientSerializer
from .utils.filters import DoubleSearchBackend


class IngredientsService(BaseService):
    instance = Ingredient
    serializer_class = IngredientSerializer
    filter_backends = [DoubleSearchBackend]
    search_fields = ['^name', '$name']
    pagination_class = None
    logger = logging.getLogger(__name__)

    # APP API logic
    def get_ingredient(self, pk: int) -> dict:
        self.logger.info('Метод IngredientsService get_ingredient вызван')
        return self.retrieve(pk=pk)
