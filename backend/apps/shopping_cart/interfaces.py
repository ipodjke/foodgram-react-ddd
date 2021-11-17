import logging

from django.http import request

import recipes.apis as recipes_api
import users.apis as users_api

logger = logging.getLogger(__name__)


class UserInterface:
    def get_user(self, pk: int) -> dict:
        logger.info('Метод UserInterface get_user вызван из shopping_cart')
        return users_api.UsersAPI().retrieve(pk=pk).data


class RecipesInrerface:
    def get_short_recipe(self, requset: request = None, pk: int = None) -> dict:
        logger.info('Метод RecipesInrerface get_user вызван из get_short_recipe')
        return recipes_api.RecipesAPI().get_short_recipe(pk=pk).data

    def get_recipe(self, request: request = None, pk: int = None) -> dict:
        logger.info('Метод RecipesInrerface get_user вызван из get_recipe')
        return recipes_api.RecipesAPI().retrieve(pk=pk).data
