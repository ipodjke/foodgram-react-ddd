from ingredients.apis import IngredientsAPI
from tags.apis import TagsAPI
from users.apis import UsersAPI


class UsersInterface:
    def get_user(self, pk: int) -> dict:
        return UsersAPI().retrieve(pk=pk).data


class TagsInterface:
    def get_tags(self, pk: int) -> dict:
        return TagsAPI().retrieve(pk=pk).data


class IngredientsInterface:
    def get_ingredient(self, pk: int) -> dict:
        return IngredientsAPI().retrieve(pk=pk).data
