import logging

import recipes.apis as recipes_api
import users.apis as users_api

logger = logging.getLogger(__name__)


class UserInterface:
    def get_user(self, pk: int) -> dict:
        logger.info('Метод UserInterface get_user вызван из subscriptions')
        return users_api.UsersAPI().retrieve(pk=pk).data


class RecipesInrerface:
    def get_author_recipes(self, author: int) -> dict:
        logger.info('Метод RecipesInrerface get_author_recipes вызван из subscriptions')
        return recipes_api.RecipesAPI().get_author_recipes(author=author).data

    def get_count_author_recipes(self, author: int) -> dict:
        logger.info('Метод RecipesInrerface get_count_author_recipes вызван из subscriptions')
        return recipes_api.RecipesAPI().get_count_author_recipes(author=author).data
