from django.http import request

from recipes.apis import RecipesAPI
from users.apis import UsersAPI


class UserInterface:
    def get_user(self, pk: int) -> dict:
        return UsersAPI().retrieve(pk=pk).data


class RecipesInrerface:
    def get_short_recipe(self, requset: request = None, pk: int = None) -> dict:
        return RecipesAPI().get_short_recipe(pk=pk).data
