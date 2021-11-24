import logging

from django.http import request

import recipes.apis as recipes_api

logger = logging.getLogger(__name__)


class RecipesInrerface:
    def get_recipe_with_shot_serializer(self, request: request, pk: int) -> dict:
        logger.info('Метод RecipesInrerface get_user вызван из get_short_recipe')
        return recipes_api.RecipesAppAPI().get_recipe_with_shot_serializer(request=request, pk=pk)

    def get_recipe(self, request: request, pk: int) -> dict:
        logger.info('Метод RecipesInrerface get_user вызван из get_recipe')
        return recipes_api.RecipesAppAPI().get_recipe(request=request, pk=pk)
