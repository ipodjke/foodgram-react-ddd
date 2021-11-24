import logging

from django.db.models.query import QuerySet
from django.http import request

import favorites.apis as favorites_api
import ingredients.apis as ingredients_api
import shopping_cart.apis as shopping_cart_api
import tags.apis as tags_api
import users.apis as user_api

logger = logging.getLogger(__name__)


class UsersInterface:
    def get_user(self, request: request, pk: int) -> dict:
        logger.info('Метод UserInterface get_user вызван из recipes')
        return user_api.UsersAppAPI().get_user(request=request, pk=pk)


class TagsInterface:
    def get_tag(self, pk: int) -> dict:
        logger.info('Метод TagsInterface get_tags вызван из recipes')
        return tags_api.TagsAppAPI().get_tag(pk=pk)

    def get_tag_by_slug(self, slug: str) -> dict:
        return tags_api.TagsAppAPI().get_tag_by_slug(slug=slug).get('id')


class IngredientsInterface:
    def get_ingredient(self, pk: int) -> dict:
        logger.info('Метод IngredientsInterface get_ingredient вызван из recipes')
        return ingredients_api.IngredientsAppAPI().get_ingredient(pk=pk)


class FavoritesInterface:
    def check_is_favorited(self, recipe: int, user: int) -> bool:
        logger.info('Метод FavoritesInterface check_is_favorited вызван из recipes')
        return favorites_api.FavoritesAppAPI().check_is_favorited(recipe=recipe, user=user)

    def get_user_favorite_recipes(self, user: int) -> QuerySet:
        logger.info('Метод FavoritesInterface get_user_favorite_recipes вызван из recipes')
        return favorites_api.FavoritesAppAPI().get_user_favorite_recipes(user=user)


class ShoppingCartInterface:
    def check_is_in_shopping_cart(self, recipe: int, user: int) -> bool:
        logger.info('Метод ShoppingCartInterface check_in_shopping_cart вызван из recipes')
        return shopping_cart_api.ShoppingCartAppAPI().check_is_in_shopping_cart(recipe=recipe,
                                                                                user=user)

    def get_user_shopping_cart(self, user: int) -> QuerySet:
        logger.info('Метод ShoppingCartInterface get_user_shopping_cart вызван из recipes')
        return shopping_cart_api.ShoppingCartAppAPI().get_user_shopping_cart(user=user)
