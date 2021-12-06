from django.db.models.query import QuerySet
from django.http import request

import recipes.apis as recipes_api
import users.apis as users_api


class RecipesInrerface:
    def get_recipe_with_shot_serializer(self, request: request, pk: int = None) -> dict:
        return recipes_api.RecipesAppAPI().get_recipe_with_shot_serializer(request=request, pk=pk)


class UsersAdminInterface:
    def get_users(self) -> QuerySet:
        return users_api.UsersAdminAPI().get_users()

    def get_user(self, pk: int) -> QuerySet:
        return users_api.UsersAdminAPI().get_user(pk=pk)


class RecipesAdminInterface:
    def get_recipes(self) -> QuerySet:
        return recipes_api.RecipesAdminAPI().get_recipes()

    def get_recipe(self, pk: int) -> QuerySet:
        return recipes_api.RecipesAdminAPI().get_recipe(pk=pk)
