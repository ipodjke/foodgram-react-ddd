import logging

from utils.base_services import BaseService

from .models import Ingredient
from .serializers import IngredientSerializer

logger = logging.getLogger(__name__)


class IngredientsService(BaseService):
    def __init__(self):
        self.instance = Ingredient

    def get_all(self) -> dict:
        logger.info('Get list of ingredients.')
        serializer = IngredientSerializer(super().get_all(), many=True)
        return serializer.data

    def get_by_id(self, instance_id: int) -> dict:
        logger.info('Get ingredient by id.')
        serializer = IngredientSerializer(super().get_by_id(instance_id))
        return serializer.data
