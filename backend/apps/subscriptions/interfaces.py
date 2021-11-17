from django.http import request

from recipes.apis import RecipesAPI
from users.apis import UsersAPI


class UserInterface:
    def get_user(self, pk: int) -> dict:
        return UsersAPI().retrieve(pk=pk).data


class RecipesInrerface:
    def get_author_recipes(self, author: int) -> dict:
        return RecipesAPI().get_author_recipes(author=author).data

    def get_count_author_recipes(self, author: int) -> dict:
        return RecipesAPI().get_count_author_recipes(author=author).data
