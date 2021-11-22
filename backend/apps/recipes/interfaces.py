import logging

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
        return user_api.UsersAPI().retrieve(request=request, pk=pk).data


class TagsInterface:
    def get_tags(self, pk: int) -> dict:
        logger.info('Метод TagsInterface get_tags вызван из recipes')
        return tags_api.TagsAPI().retrieve(pk=pk).data
    
    def get_tag_by_slug(self, slug: str) -> int:
        return tags_api.TagsAPI().get_tag_by_slug(slug=slug).data.get('id')


class IngredientsInterface:
    def get_ingredient(self, pk: int) -> dict:
        logger.info('Метод IngredientsInterface get_ingredient вызван из recipes')
        return ingredients_api.IngredientsAPI().retrieve(pk=pk).data


class FavoritesInterface:
    def check_is_favorited(self, recipe: int, user: int) -> dict:
        logger.info('Метод FavoritesInterface check_is_favorited вызван из recipes')
        return favorites_api.FavoritesAPI().check_is_favorited(recipe=recipe, user=user).data

    def get_user_favorite_recipes(self, user: int) -> dict:
        logger.info('Метод FavoritesInterface get_user_favorite_recipes вызван из recipes')
        return favorites_api.FavoritesAPI().get_user_favorite_recipes(user=user).data


class ShoppingCartInterface:
    def check_is_in_shopping_cart(self, recipe: int, user: int) -> dict:
        logger.info('Метод ShoppingCartInterface check_in_shopping_cart вызван из recipes')
        return shopping_cart_api.ShoppingCartAPI().check_is_in_shopping_cart(recipe=recipe,
                                                                             user=user).data

    def get_user_shopping_cart(self, user: int) -> dict:
        logger.info('Метод ShoppingCartInterface get_user_shopping_cart вызван из recipes')
        return shopping_cart_api.ShoppingCartAPI().get_user_shopping_cart(user=user).data
