import logging

from django.http import request

import recipes.apis as recipes_api
import users.apis as users_api

logger = logging.getLogger(__name__)


class UserInterface:
    def get_user(self, pk: int) -> dict:
        logger.info('Метод UserInterface get_user вызван из favorites')
        return users_api.UsersAPI().retrieve(pk=pk).data


class RecipesInrerface:
    def get_short_recipe(self, requset: request = None, pk: int = None) -> dict:
        logger.info('Метод RecipesInrerface get_short_recipe вызван из favorites')
        return recipes_api.RecipesAPI().get_short_recipe(pk=pk).data
