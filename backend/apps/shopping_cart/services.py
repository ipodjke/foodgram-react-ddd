import io
import logging

from django.conf import settings
from django.db.models.query import QuerySet
from django.http import request

import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.exceptions import ValidationError

from utils.base_services import BaseService

from .interfaces import RecipesInrerface
from .models import ShoppingCart

logger = logging.getLogger(__name__)


class ShoppingCartService(BaseService):
    def __init__(self):
        self.instance = ShoppingCart

    def add_to_shopping_cart(self, request: request, pk: int = None) -> dict:
        logger.info('Метод ShoppingCartService add_to_shopping_cart вызван')
        if self.instance.objects.filter(user=request.user.id, recipe=pk).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('alredy_in_cart')}
            )
        self.instance.objects.create(user=request.user.id, recipe=pk)
        return RecipesInrerface().get_short_recipe(pk=pk)

    def delete_from_shopping_cart(self, request: request, pk: int = None) -> bool:
        logger.info('Метод ShoppingCartService delete_from_shopping_cart вызван')
        if not self.instance.objects.filter(user=request.user.id, recipe=pk).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('not_in_cart')}
            )
        self.instance.objects.get(user=request.user.id, recipe=pk).delete()
        return True

    def check_is_in_shopping_cart(self, recipe: int, user: int) -> bool:
        logger.info('Метод ShoppingCartService check_is_in_shopping_cart вызван')
        return self.instance.objects.filter(user=user, recipe=recipe).exists()

    def get_user_shopping_cart(self, user: int) -> dict:
        logger.info('Метод ShoppingCartService get_user_shopping_cart вызван')
        return self.instance.objects.filter(user=user)

    def download_shopping_cart(self, request: request) -> dict:
        logger.info('Метод download_shopping_cart delete_from_shopping_cart вызван')
        shopping_cart = self.instance.objects.filter(user=request.user.id)
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
            ingredients = RecipesInrerface().get_recipe(pk=recipe.recipe).get('ingredients')
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
