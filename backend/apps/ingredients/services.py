import logging

from django.http import request

from utils.base_services import BaseService
from utils.filters import DoubleSearchBackend

from .models import Ingredient
from .serializers import IngredientSerializer

logger = logging.getLogger(__name__)


class IngredientsService(BaseService):

    filter_backends = [DoubleSearchBackend]
    search_fields = ['^name', '$name']

    def __init__(self):
        self.instance = Ingredient

    def get_all(self, request: request) -> dict:
        logger.info('Метод IngredientsService get_all вызван')
        queryset = self.filter_queryset(super().get_all(), request)
        serializer = IngredientSerializer(queryset, many=True)
        return serializer.data

    def get_by_id(self, instance_id: int) -> dict:
        logger.info('Метод IngredientsService get_by_id вызван')
        serializer = IngredientSerializer(super().get_by_id(instance_id))
        return serializer.data

    def filter_queryset(self, queryset, request):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset
