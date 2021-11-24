import logging

from django.db.models.query import QuerySet
from django.http import request

import recipes.apis as recipes_api
import users.apis as users_api

logger = logging.getLogger(__name__)


class UserInterface:
    def get_user(self, request: request, pk: int) -> dict:
        logger.info('Метод UserInterface get_user вызван из subscriptions')
        return users_api.UsersAppAPI().get_user(pk=pk, request=request)


class RecipesInrerface:
    def get_author_recipes(self, author: int) -> QuerySet:
        logger.info('Метод RecipesInrerface get_author_recipes вызван из subscriptions')
        return recipes_api.RecipesAppAPI().get_author_recipes(author=author)

    def get_count_author_recipes(self, author: int) -> int:
        logger.info('Метод RecipesInrerface get_count_author_recipes вызван из subscriptions')
        return recipes_api.RecipesAppAPI().get_count_author_recipes(author=author)
