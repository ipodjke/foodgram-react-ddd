import io

from django.conf import settings
from django.http import FileResponse

import reportlab
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from utils.filters import (IsDownloadFilterBackend, IsFavoritedFilterBackend,
                           RecipeFilterSet)
from utils.generalizing_functions import (check_the_occurrence,
                                          send_bad_request_response)
from utils.permissions import IsOwnerOrReadOnly

from .models import MarkedUserRecipes, Recipe
from .srializers import (CreateRecipeSerializer, RecipeSerializer,
                         ShortRecipeSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [
        DjangoFilterBackend,
        IsFavoritedFilterBackend,
        IsDownloadFilterBackend,
    ]
    filterset_class = RecipeFilterSet
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if (self.action == 'create'
                or self.action == 'update' or self.action == 'partial_update'):
            return CreateRecipeSerializer
        return super().get_serializer_class()

    # def partial_update(self, request, *args, **kwargs):
    #     return Response(
    #         {'detail': 'Метод PATCH не разрешен.'},
    #         status=status.HTTP_405_METHOD_NOT_ALLOWED
    #     )

    @action(detail=True, serializer_class=ShortRecipeSerializer,
            url_path='favorite', permission_classes=[IsAuthenticated])
    def mark_favorite_recipe(self, request, id=None, *args, **kwargs):
        return self._mark_recipes(request, id=None, *args, **kwargs)

    @mark_favorite_recipe.mapping.delete
    def delete_favorite_recipe(self, request, id=None, *args, **kwargs):
        return self._delete_mark_recipes(request, id=None, *args, **kwargs)

    @action(detail=True, serializer_class=ShortRecipeSerializer,
            url_path='shopping_cart', permission_classes=[IsAuthenticated])
    def mark_download_recipe(self, request, id=None, *args, **kwargs):
        return self._mark_recipes(request, id=None, *args, **kwargs)

    @mark_download_recipe.mapping.delete
    def delete_download_recipe(self, request, id=None, *args, **kwargs):
        return self._delete_mark_recipes(request, id=None, *args, **kwargs)

    def _mark_recipes(self, request, id=None, *args, **kwargs):
        """
        Добавить рецепт в список избранного/список загрузок

        Добавляет в нужный список выбранный рецеп, следит за наличием
        данного рецепта, в случае наличия отсылает соответсвующий ответ.
        """
        marked_recipes, _ = MarkedUserRecipes.objects.get_or_create(
                                                            user=request.user
                                                        )
        recipe = self.get_object()

        if request.path.split('/')[-2] == 'favorite':
            if check_the_occurrence(recipe,
                                    'fovorited_recipe',
                                    marked_recipes):

                return send_bad_request_response(
                    settings.ERROR_MESSAGE.get('alredy_favorited')
                )

            marked_recipes.fovorited_recipe.add(recipe)
        else:
            if check_the_occurrence(recipe,
                                    'recipe_for_download',
                                    marked_recipes):

                return send_bad_request_response(
                    settings.ERROR_MESSAGE.get('alredy_in_cart')
                )

            marked_recipes.recipe_for_download.add(recipe)

        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete_mark_recipes(self, request, id=None, *args, **kwargs):
        """
        Удалить рецепт из списка избранного/списка загрузок

        Удаляет из нужнгого списка выбранный рецеп, следит за наличием
        данного рецепта, в случае отсутствия отсылает соответсвующий ответ.
        """
        marked_recipes, _ = MarkedUserRecipes.objects.get_or_create(
                                                            user=request.user
                                                        )
        recipe = self.get_object()

        if request.path.split('/')[-2] == 'favorite':
            if not check_the_occurrence(recipe,
                                        'fovorited_recipe',
                                        marked_recipes):

                return send_bad_request_response(
                    settings.ERROR_MESSAGE.get('not_in_favorited')
                )
            marked_recipes.fovorited_recipe.remove(recipe.id)
        else:
            if not check_the_occurrence(recipe,
                                        'recipe_for_download',
                                        marked_recipes):

                return send_bad_request_response(
                    settings.ERROR_MESSAGE.get('alredy_in_cart')
                )

            marked_recipes.recipe_for_download.remove(recipe.id)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, url_path='download_shopping_cart',
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request, *args, **kwargs):
        shopping_cart = request.user.marked_recipes.recipe_for_download.all()
        ingredient_list = self._get_ingredient_list(shopping_cart)
        return self._send_file_response(ingredient_list)

    def _get_ingredient_list(self, shopping_cart: list) -> dict:
        """
        Получить список ингредиентов.

        Сформировывает словарь из ингредиентов всех рецептов вида:
            {имя (единица измерения): колличество}
        -----
        Note:
            Одинаковые ингредиенты складываются и хранятся ввиде
            суммы под одним ключем.
        -----
        Параметры:
            shopping_cart: list - список обьектов Recipe
        -----
        выходное значение
            dict: словарь ингредиентов ввида:
                {имя (единица измерения): колличество}
        """
        ingredient_list = {}

        for recipe in shopping_cart:
            ingredients = recipe.ingredients.through.objects.filter(
                                                                recipe=recipe
                                                            )
            for ingredient in ingredients:
                key = (f'{ingredient.ingredients.name} '
                       f'({ingredient.ingredients.measurement_unit})')
                try:
                    ingredient_list[key] += ingredient.amount
                except KeyError:
                    ingredient_list[key] = ingredient.amount

        return ingredient_list

    def _send_file_response(self, ingredient_list: dict) -> object:
        """
        Отправить свормированый файл.

        Формирует файл(pdf) на онсове ingredient_list и отправляет его

        ------
        Параметры:
            ingredient_list: dict - словарь ингредиентов ввида:
                {имя (единица измерения): колличество}
        -----
        Выходное значение:
            object - FileResponse
        """
        reportlab.rl_config.TTFSearchPath.append(
            str(settings.BASE_DIR) + '/utils/fonts/'
        )
        pdfmetrics.registerFont(TTFont('Roboto', 'Roboto.ttf'))

        buffer = io.BytesIO()
        p = canvas.Canvas(
            buffer,
            pagesize=A4,
            initialFontName='Roboto',
            initialFontSize=18
        )

        margin_top = 27 * cm
        margint_top_header = margin_top - 3 * cm
        left_margin = 1 * cm

        p.drawString(6.5 * cm, margin_top, 'Общий список ингредиентов!')
        p.setFontSize(16)

        for ingredient, amount in ingredient_list.items():
            p.drawString(
                left_margin,
                margint_top_header,
                f'{ingredient} - {amount}'
            )
            margint_top_header -= cm

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='product_list.pdf'
        )
