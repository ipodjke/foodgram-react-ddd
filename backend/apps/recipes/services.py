import logging
from collections import OrderedDict

from django.db.models.query import QuerySet
from django.http import request

from rest_framework import serializers
from rest_framework.settings import api_settings

from utils.base_services import BaseService

from .interfaces import IngredientsInterface, TagsInterface, UsersInterface
from .models import RecipeNew
from .serializers import (CreateRecipeSerializerNew, RecipeSerializerNew,
                          ShortRecipeSerializerNew)

logger = logging.getLogger(__name__)


class RecipesService(BaseService):
    def __init__(self):
        self.instance = RecipeNew
        self.pagination_class = api_settings.DEFAULT_PAGINATION_CLASS()

    def get_pagination_list(self, request: request) -> dict:
        logger.info('Get pagination recipe list.')
        queryset = self.instance.objects.all()
        page = self.pagination_class.paginate_queryset(queryset=queryset, request=request, view=None)
        serializer = RecipeSerializerNew(page, many=True)
        return OrderedDict([
            ('count', self.pagination_class.page.paginator.count),
            ('next', self.pagination_class.get_next_link()),
            ('previous', self.pagination_class.get_previous_link()),
            ('result', serializer.data)
        ])

    def create_recipe(self, request: request) -> dict:
        serializer = CreateRecipeSerializerNew(
            data=request.data,
            context={'author': request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get_user(self, pk: int) -> dict:
        return UsersInterface().get_user(pk=pk)

    def get_tags(self, tags: QuerySet) -> list:
        return [TagsInterface().get_tags(pk=tag.tag) for tag in tags]

    def get_ingredient(self, pk: int) -> dict:
        return IngredientsInterface().get_ingredient(pk=pk)

    def get_by_id(self, pk: int) -> dict:
        logger.info('Get ingredient by id.')
        serializer = RecipeSerializerNew(super().get_by_id(instance_id=pk))
        return serializer.data

    def delete(self, pk: int) -> bool:
        logger.info('Delete recipe.')
        return super().delete(instance_id=pk)

    def update(self, request: request, pk: int, **kwargs) -> dict:
        logger.info('Update recipe.')
        partial = kwargs.pop('partial', False)
        instance = super().get_by_id(instance_id=pk)
        serializer = CreateRecipeSerializerNew(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get_short_recipe_list(self, author: int) -> dict:
        logger.info('Get author recipes.')
        queryset = self.instance.objects.filter(author=author)
        serializer = ShortRecipeSerializerNew(queryset, many=True)
        return serializer.data

    def get_count_author_recipes(self, author: int) -> dict:
        logger.info('Get count author recipes.')
        return {'count': self.instance.objects.filter(author=author).count()}

    def get_short_recipe(self, pk: int) -> dict:
        instance = self.instance.objects.get(id=pk)
        serializer = ShortRecipeSerializerNew(instance)
        return serializer.data
