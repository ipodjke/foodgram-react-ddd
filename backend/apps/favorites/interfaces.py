import logging

from django.http import request

import recipes.apis as recipes_api

logger = logging.getLogger(__name__)


class RecipesInrerface:
    def get_recipe_with_shot_serializer(self, request: request, pk: int = None) -> dict:
        logger.info('Метод RecipesInrerface get_short_recipe вызван из favorites')
        return recipes_api.RecipesAppAPI().get_recipe_with_shot_serializer(request=request, pk=pk)
