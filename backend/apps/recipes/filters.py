from django.conf import settings

from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import BaseFilterBackend

import recipes.services as service

from .models import Recipe, TagsList


class IsFavoritedFilterBackend(BaseFilterBackend):
    """
    Фильтр для вывода избраных рецептов пользователя.

    Интегрирована с другими фильтрами и пагинацией.
    """
    def filter_queryset(self, request, queryset, view):
        path_name = settings.PATH_PARAM_NAMES.get('favorited')
        if request.query_params.get(path_name) == 'true':
            favorite_recipes = service.RecipesService().get_user_favorite_recipes(user=request.user)
            result = []
            for recipe in favorite_recipes:
                for obj in queryset:
                    if recipe.recipe == obj.id:
                        result.append(obj)
                        break
            return result
        return queryset


class IsInShopponCartFilterBackend(BaseFilterBackend):
    """
    Фильтр для вывода рецептов из корзины пользователя.

    Подерживает установленную пагинацию с ее фильтрами.
    Приорететней над базовыми drf фильтрами.
    """
    def filter_queryset(self, request, queryset, view):
        path_name = settings.PATH_PARAM_NAMES.get('shopping_cart')

        if request.query_params.get(path_name) == 'true':
            favorite_recipes = service.RecipesService().get_user_shopping_cart(user=request.user)
            result = []
            for recipe in favorite_recipes:
                for obj in queryset:
                    if recipe.recipe == obj.id:
                        result.append(obj)
                        break
            return result
        return queryset


class RecipeFilterSet(FilterSet):
    """
    Фильтерсет для кастомной фильтрации.

    Переопределено поведение фильтрации с поля id на slug при
    фильтрации по tags.
    При фильтрации по author фильтрация идет по id.
    """
    tags = filters.CharFilter(
        method='filter_on_tags'
    )

    def filter_on_tags(self, queryset, name, value):
        tags = service.RecipesService().get_tags_by_slug(self.request.query_params.getlist('tags'))
        return queryset.filter(tags__tag__in=tags).distinct()

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
