from django.db.models.query import QuerySet
from django.http import request

import favorites.apis as favorites_api
import ingredients.apis as ingredients_api
import shopping_cart.apis as shopping_cart_api
import tags.apis as tags_api
import users.apis as user_api


class UsersInterface:
    def get_user(self, request: request, pk: int) -> dict:
        return user_api.UsersAppAPI().get_user(request=request, pk=pk)


class TagsInterface:
    def get_tag(self, pk: int) -> dict:
        return tags_api.TagsAppAPI().get_tag(pk=pk)

    def get_tag_by_slug(self, slug: str) -> dict:
        return tags_api.TagsAppAPI().get_tag_by_slug(slug=slug).get('id')


class IngredientsInterface:
    def get_ingredient(self, pk: int) -> dict:
        return ingredients_api.IngredientsAppAPI().get_ingredient(pk=pk)


class FavoritesInterface:
    def check_is_favorited(self, recipe: int, user: int) -> bool:
        return favorites_api.FavoritesAppAPI().check_is_favorited(recipe=recipe, user=user)

    def get_user_favorite_recipes(self, user: int) -> QuerySet:
        return favorites_api.FavoritesAppAPI().get_user_favorite_recipes(user=user)


class ShoppingCartInterface:
    def check_is_in_shopping_cart(self, recipe: int, user: int) -> bool:
        return shopping_cart_api.ShoppingCartAppAPI().check_is_in_shopping_cart(recipe=recipe,
                                                                                user=user)

    def get_user_shopping_cart(self, user: int) -> QuerySet:
        return shopping_cart_api.ShoppingCartAppAPI().get_user_shopping_cart(user=user)


class UsersAdminInterface:
    def get_users(self) -> QuerySet:
        return user_api.UsersAdminAPI().get_users()

    def get_user(self, pk: int) -> QuerySet:
        return user_api.UsersAdminAPI().get_user(pk=pk)


class IngredientsAdminInterface:
    def get_ingredients(self) -> QuerySet:
        return ingredients_api.IngredientsAdminAPI().get_ingredients()


class TagsAdminInterface:
    def get_tags(self) -> QuerySet:
        return tags_api.TagsAdminAPI().get_tags()


class FavoritesAdminInterface:
    def get_total_number_of_additions(self, pk: int) -> int:
        return favorites_api.FavoritesAdminAPI().get_total_number_of_additions(pk=pk)
