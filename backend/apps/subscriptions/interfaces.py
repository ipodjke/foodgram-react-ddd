from django.db.models.query import QuerySet
from django.http import request

import recipes.apis as recipes_api
import users.apis as users_api


class UserInterface:
    def get_user(self, request: request, pk: int) -> dict:
        return users_api.UsersAppAPI().get_user(pk=pk, request=request)


class RecipesInrerface:
    def get_author_recipes(self, author: int) -> QuerySet:
        return recipes_api.RecipesAppAPI().get_author_recipes(author=author)

    def get_count_author_recipes(self, author: int) -> int:
        return recipes_api.RecipesAppAPI().get_count_author_recipes(author=author)


class UsersAdminInterface:
    def get_user(self, pk: int) -> QuerySet:
        return users_api.UsersAdminAPI().get_user(pk=pk)

    def get_users(self) -> QuerySet:
        return users_api.UsersAdminAPI().get_users()
