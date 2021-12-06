import io
import logging
from typing import Union

from django.conf import settings
from django.db.models.query import QuerySet
from django.http.response import Http404

import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.exceptions import ValidationError

import shopping_cart.interfaces as interface
from utils.base_services import BaseService

from .models import ShoppingCart
from .serializers import ShoppingCartSerializer

logger = logging.getLogger(__name__)


class ShoppingCartService(BaseService):
    instance = ShoppingCart
    serializer_class = ShoppingCartSerializer
    lookup_field = 'recipe'
    lookup_url_kwarg = 'pk'
    include_to_lookup = {'user': 'self.request.user.id'}
    filter_backends = []
    pagination_class = None

    # REST API logic
    def add_to_shopping_cart(self, pk: int) -> dict:
        logger.info('Метод ShoppingCartService add_to_shopping_cart вызван')
        # recipe ловим Http404 exception, не возможно добавить не существующий рецепт.
        recipe = interface.RecipesInrerface().get_recipe_with_shot_serializer(request=self.request,
                                                                              pk=pk)
        data = {
            'user': self.request.user.id,
            'recipe': pk
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return recipe # noqa

    def delete_from_shopping_cart(self, pk: int = None) -> bool:
        logger.info('Метод ShoppingCartService delete_from_shopping_cart вызван')
        self._validate_delete_request(user=self.request.user.id, recipe=pk)
        self.get_object().delete()
        return True

    def download_shopping_cart(self) -> dict:
        logger.info('Метод download_shopping_cart delete_from_shopping_cart вызван')
        shopping_cart = self.instance.objects.filter(user=self.request.user.id)
        ingredients = self._get_ingredients(shopping_cart)
        file = self._create_file(ingredients)
        return self._create_file_response(file)

    def _get_ingredients(self, shopping_cart: QuerySet) -> dict:
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
            shopping_cart: QuerySet - список обьектов Recipe
        -----
        выходное значение
            dict: словарь ингредиентов ввида:
                {имя (единица измерения): колличество}
        """
        ingredient_list = {}

        for recipe in shopping_cart:
            ingredients = interface.RecipesInrerface().get_recipe(
                pk=recipe.recipe,
                request=self.request,
            ).get('ingredients')

            for ingredient in ingredients:
                key = (f'{ingredient.get("name")} '
                       f'({ingredient.get("measurement_unit")})')
                try:
                    ingredient_list[key] += ingredient.get('amount')
                except KeyError:
                    ingredient_list[key] = ingredient.get('amount')
        return ingredient_list

    def _create_file(self, ingredients: dict) -> dict:
        """
        Сформировать файл.

        Формирует файл(pdf) на онсове ingredients

        ------
        Параметры:
            ingredients: dict - словарь ингредиентов ввида:
                {имя (единица измерения): колличество}
        -----
        Выходное значение:
            object - pdf файл
        """
        reportlab.rl_config.TTFSearchPath.append('./apps/shopping_cart/utils/fonts/')
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

        p.drawString(5.3 * cm, margin_top, 'Ингредиенты для похода в магазин! :)')
        p.setFontSize(16)

        for ingredient, amount in ingredients.items():
            p.drawString(
                left_margin,
                margint_top_header,
                f'{ingredient} - {amount}'
            )
            margint_top_header -= cm

        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

    def _create_file_response(self, file: io.BytesIO) -> dict:
        """
        Создать словарь с параметрами для FileResponse.
        """
        return {
            'file': file,
            'as_attachment': True,
            'filename': 'product_list.pdf'
        }

    # APP API logic
    def check_is_in_shopping_cart(self, recipe: int, user: int) -> bool:
        logger.info('Метод ShoppingCartService check_is_in_shopping_cart вызван')
        context = {'user': user, 'recipe': recipe}
        return self.check_is_in(context)

    def get_user_shopping_cart(self, user: int) -> QuerySet:
        logger.info('Метод ShoppingCartService get_user_shopping_cart вызван')
        return self.instance.objects.filter(user=user)

    # local functions
    def _validate_delete_request(self, user: int, recipe: int) -> Union[ValidationError,
                                                                        Http404,
                                                                        None]:
        print(11111)
        interface.RecipesInrerface().get_recipe_with_shot_serializer(request=self.request,
                                                                     pk=recipe)
        if not self.instance.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('not_in_cart')}
            )


class ShoppingCartAdminService:
    # interface logic
    # Recipes
    def get_recipes(self) -> QuerySet:
        logger.info('Метод ShoppingCartAdminService get_recipes вызван')
        return interface.RecipesAdminInterface().get_recipes()

    def get_recipe(self, pk: int) -> QuerySet:
        logger.info('Метод ShoppingCartAdminService get_recipe вызван')
        return interface.RecipesAdminInterface().get_recipe(pk=pk)

    # Users
    def get_users(self) -> QuerySet:
        logger.info('Метод ShoppingCartAdminService get_users вызван')
        return interface.UsersAminInterface().get_users()

    def get_user(self, pk: int) -> QuerySet:
        logger.info('Метод ShoppingCartAdminService get_user вызван')
        return interface.UsersAminInterface().get_user(pk=pk)
