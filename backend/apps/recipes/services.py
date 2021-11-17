import logging
from collections import OrderedDict

from django.db.models.query import QuerySet
from django.http import request
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.settings import api_settings

import recipes.interfaces as interfaces
from utils.base_services import BaseService

from .filters import (IsFavoritedFilterBackend, IsInShopponCartFilterBackend,
                      RecipeFilterSet)
from .models import Recipe
from .serializers import (CreateRecipeSerializer, RecipeSerializer,
                          ShortRecipeSerializer)

logger = logging.getLogger(__name__)


class RecipesService(BaseService):

    filter_backends = [
        DjangoFilterBackend,
        IsFavoritedFilterBackend,
        IsInShopponCartFilterBackend,
    ]
    filterset_class = RecipeFilterSet

    def __init__(self):
        self.instance = Recipe
        self.pagination_class = api_settings.DEFAULT_PAGINATION_CLASS()

    def get_pagination_list(self, request: request) -> dict:
        logger.info('Метод RecipesService get_pagination_list вызван')
        queryset = self.filter_queryset(self.instance.objects.all(), request)

        page = self.pagination_class.paginate_queryset(
            queryset=queryset,
            request=request,
            view=None
        )

        serializer = RecipeSerializer(page, many=True, context={'request': request})
        return OrderedDict([
            ('count', self.pagination_class.page.paginator.count),
            ('next', self.pagination_class.get_next_link()),
            ('previous', self.pagination_class.get_previous_link()),
            ('result', serializer.data)
        ])

    def create_recipe(self, request: request) -> dict:
        logger.info('Метод RecipesService create_recipe вызван')
        serializer = CreateRecipeSerializer(
            data=request.data,
            context={'author': request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get_user(self, request: request, pk: int) -> dict:
        logger.info('Метод RecipesService get_user вызван')
        return interfaces.UsersInterface().get_user(request=request, pk=pk)

    def get_tags(self, tags: QuerySet) -> list:
        logger.info('Метод RecipesService get_tags вызван')
        return [interfaces.TagsInterface().get_tags(pk=tag.tag) for tag in tags]

    def get_ingredient(self, pk: int) -> dict:
        logger.info('Метод RecipesService get_ingredient вызван')
        return interfaces.IngredientsInterface().get_ingredient(pk=pk)

    def get_by_id(self, pk: int) -> dict:
        logger.info('Метод RecipesService get_by_id вызван')
        serializer = RecipeSerializer(super().get_by_id(instance_id=pk))
        return serializer.data

    def delete(self, request: request, pk: int) -> bool:
        logger.info('Метод RecipesService delete вызван')
        instance = get_object_or_404(self.instance, pk=pk)

        if request.user.id != instance.author:
            raise PermissionDenied('Тлолько автор может удалять рецет')

        instance.delete()
        return True

    def update(self, request: request, pk: int, **kwargs) -> dict:
        logger.info('Метод RecipesService update вызван')
        partial = kwargs.pop('partial', False)
        instance = super().get_by_id(instance_id=pk)

        if request.user.id != instance.author:
            raise PermissionDenied('Тлолько автор может обновлять рецет')

        serializer = CreateRecipeSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get_short_recipe_list(self, author: int) -> dict:
        logger.info('Метод RecipesService get_short_recipe_list вызван')
        queryset = self.instance.objects.filter(author=author)
        serializer = ShortRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_count_author_recipes(self, author: int) -> dict:
        logger.info('Метод RecipesService get_count_author_recipes вызван')
        return {'count': self.instance.objects.filter(author=author).count()}

    def get_short_recipe(self, pk: int) -> dict:
        logger.info('Метод RecipesService get_short_recipe вызван')
        instance = self.instance.objects.get(id=pk)
        serializer = ShortRecipeSerializer(instance)
        return serializer.data

    def check_is_favorited(self, recipe: int, user: object) -> bool:
        logger.info('Метод RecipesService get_short_recipe вызван')

        if user is None or user.is_anonymous:
            return False

        return interfaces.FavoritesInterface().check_is_favorited(recipe=recipe, user=user.id)

    def check_is_in_shopping_cart(self, recipe: int, user: object) -> bool:
        logger.info('Метод RecipesService check_in_shopping_cart вызван')

        if user is None or user.is_anonymous:
            return False

        return interfaces.ShoppingCartInterface().check_is_in_shopping_cart(recipe=recipe,
                                                                            user=user.id)

    def get_user_favorite_recipes(self, user: object) -> dict:
        logger.info('Метод RecipesService get_user_favorite_recipes вызван')
        if user.is_anonymous:
            return {}
        return interfaces.FavoritesInterface().get_user_favorite_recipes(user=user.id)

    def get_user_shopping_cart(self, user: object) -> dict:
        logger.info('Метод RecipesService get_user_shopping_cart вызван')
        if user.is_anonymous:
            return {}
        return interfaces.ShoppingCartInterface().get_user_shopping_cart(user=user.id)

    def filter_queryset(self, queryset, request):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset
