from django.conf import settings
from django_filters.rest_framework import FilterSet, filters
from rest_framework.exceptions import ValidationError

import recipes.services as service
from recipes.models import Recipe


class RecipeFilterSet(FilterSet):
    """
    Фильтерсет для кастомной фильтрации.

    Фильтрация идет по следующим query праметрам:
    - author: указывается id автора рецепта
    - tags: указывается slug тега(ов)
    - is_favorited: true, выводит список рецептов из избранного
    - is_in_shopping_cart: true, выводит список рецептов из корзины

    Note:
    --------
    is_favorited и is_in_shopping_cart - самостоятельные параметры, совместное
    использование, в том числе с author приводит к возвращениее HTTP404_BAD_REQUEST
    """
    tags = filters.CharFilter(
        method='filter_on_tags'
    )
    is_favorited = filters.CharFilter(
        method='check_is_in_favorited'
    )
    is_in_shopping_cart = filters.CharFilter(
        method='check_is_in_shopping_cart'
    )

    def filter_on_tags(self, queryset, name, value):
        tags = service.RecipesService().get_tags_by_slug(self.request.query_params.getlist('tags'))
        return queryset.filter(tags__tag__in=tags).distinct()

    def check_is_in_favorited(self, queryset, name, value):
        path_name = settings.PATH_PARAM_NAMES.get('favorited')

        if self.request.query_params.get(path_name) == 'true':
            favorite_recipes = service.RecipesService().get_user_favorite_recipes(
                user=self.request.user
            )

            return queryset.filter(id__in=[value[0]for value in favorite_recipes.values_list('recipe')]) # noqa

        return queryset

    def check_is_in_shopping_cart(self, queryset, name, value):
        path_name = settings.PATH_PARAM_NAMES.get('shopping_cart')

        if self.request.query_params.get(path_name) == 'true':
            favorite_recipes = service.RecipesService().get_user_shopping_cart(
                user=self.request.user
            )

            return queryset.filter(id__in=[value[0]for value in favorite_recipes.values_list('recipe')]) # noqa

        return queryset

    def is_valid(self):
        shopping_cart = self.request.query_params.get(
            settings.PATH_PARAM_NAMES.get('shopping_cart')
        )
        favorited = self.request.query_params.get(
            settings.PATH_PARAM_NAMES.get('favorited')
        )

        if shopping_cart and favorited:
            raise ValidationError({'error': settings.ERROR_MESSAGE.get('both_query_params')})
        elif (shopping_cart or favorited) and self.request.query_params.get('author'):
            raise ValidationError({'error': settings.ERROR_MESSAGE.get('unique_query_params')})

        return super().is_valid()

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
