import logging
from typing import Union

from django.db.models.query import QuerySet
from django.http import request

from django_filters.rest_framework import DjangoFilterBackend

import recipes.interfaces as interfaces
from utils.base_services import BaseService

from .models import Recipe
from .serializers import (CreateRecipeSerializer, RecipeSerializer,
                          ShortRecipeSerializer)
from .utils.filters import RecipeFilterSet
from .utils.permission import IsOwnerUpateOrDelete

logger = logging.getLogger(__name__)


class RecipesService(BaseService):
    instance = Recipe
    serializer_class = RecipeSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_class = RecipeFilterSet
    permission_classes = [IsOwnerUpateOrDelete]

    # REST API logic
    def update(self, pk: int, **kwargs) -> dict:
        logger.info('Метод RecipesService update вызван')
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=self.request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    # APP API logic
    def get_recipes_with_short_serializer(self, author: int) -> dict:
        logger.info('Метод RecipesService get_recipes_with_short_serializer вызван')
        queryset = self.instance.objects.filter(author=author)
        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    def get_count_author_recipes(self, author: int) -> int:
        logger.info('Метод RecipesService get_count_author_recipes вызван')
        return self.instance.objects.filter(author=author).count()

    def get_recipe_with_shot_serializer(self, pk: int) -> dict:
        logger.info('Метод RecipesService get_short_recipe вызван')
        return self.retrieve(pk=pk)

    def get_recipe(self, pk: int) -> dict:
        logger.info('Метод RecipesService get_recipe вызван')
        return self.retrieve(pk=pk)

    # interface logic
    # Users
    def get_user(self, request: request, pk: int) -> dict:
        logger.info('Метод RecipesService get_user вызван')
        return interfaces.UsersInterface().get_user(request=request, pk=pk)

    # Tags
    def get_tags(self, tags: QuerySet) -> list:
        logger.info('Метод RecipesService get_tags вызван')
        return [interfaces.TagsInterface().get_tag(pk=tag.tag) for tag in tags]

    def get_tags_by_slug(self, slugs: list) -> list:
        return [interfaces.TagsInterface().get_tag_by_slug(slug=slug) for slug in slugs]

    # Ingredients
    def get_ingredient(self, pk: int) -> dict:
        logger.info('Метод RecipesService get_ingredient вызван')
        return interfaces.IngredientsInterface().get_ingredient(pk=pk)

    # Favorites
    def check_is_favorited(self, recipe: int, user: object) -> bool:
        logger.info('Метод RecipesService check_is_favorited вызван')

        if user is None or user.is_anonymous:
            return False

        return interfaces.FavoritesInterface().check_is_favorited(recipe=recipe, user=user.id)

    def get_user_favorite_recipes(self, user: object) -> Union[QuerySet, dict]:
        logger.info('Метод RecipesService get_user_favorite_recipes вызван')
        if user.is_anonymous:
            return {}
        return interfaces.FavoritesInterface().get_user_favorite_recipes(user=user.id)

    # Shopping cart
    def check_is_in_shopping_cart(self, recipe: int, user: object) -> bool:
        logger.info('Метод RecipesService check_in_shopping_cart вызван')

        if user is None or user.is_anonymous:
            return False

        return interfaces.ShoppingCartInterface().check_is_in_shopping_cart(recipe=recipe,
                                                                            user=user.id)

    def get_user_shopping_cart(self, user: object) -> Union[QuerySet, dict]:
        logger.info('Метод RecipesService get_user_shopping_cart вызван')
        if user.is_anonymous:
            return {}
        return interfaces.ShoppingCartInterface().get_user_shopping_cart(user=user.id)

    # Service logic
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return CreateRecipeSerializer
        elif self.action == 'short_serializer':
            return ShortRecipeSerializer
        return super().get_serializer_class()


class RecipesAdminService:
    instance = Recipe

    def get_recipes(self) -> QuerySet:
        logger.info('Метод RecipesAdminService get_recipes вызван')
        return self.instance.objects.all()

    def get_recipe(self, pk: int) -> QuerySet:
        logger.info('Метод RecipesAdminService get_recipe вызван')
        return self.instance.objects.get(pk=pk)

    # interface logic
    # Users
    def get_users(self) -> QuerySet:
        logger.info('Метод RecipesAdminService get_users вызван')
        return interfaces.UsersAdminInterface().get_users()

    def get_user(self, pk: int) -> QuerySet:
        logger.info('Метод RecipesAdminService get_user вызван')
        return interfaces.UsersAdminInterface().get_user(pk=pk)

    # Ingredients
    def get_ingredients(self) -> QuerySet:
        logger.info('Метод RecipesAdminService get_ingredients вызван')
        return interfaces.IngredientsAdminInterface().get_ingredients()

    # Tags
    def get_tags(self) -> QuerySet:
        logger.info('Метод RecipesAdminService get_tags вызван')
        return interfaces.TagsAdminInterface().get_tags()

    # Favorites
    def get_total_number_of_additions(self, pk: int) -> int:
        logger.info('Метод RecipesAdminService get_total_number_of_additions вызван')
        return interfaces.FavoritesAdminInterface().get_total_number_of_additions(pk=pk)
