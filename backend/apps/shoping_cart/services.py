import io
import logging
from collections import OrderedDict
from re import A

from django.conf import settings
from django.db.models.query import QuerySet
from django.http import request

import reportlab
import subscriptions.services as service
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from recipes.interfaces import UsersInterface
from utils.base_services import BaseService

from .interfaces import RecipesInrerface, UserInterface
from .models import ShopingCart
from .serializers import SubscriptionsSerializer

logger = logging.getLogger(__name__)


class ShopingCartService(BaseService):
    def __init__(self):
        self.instance = ShopingCart

    def add_to_shoping_cart(self, request: request, pk: int = None) -> dict:
        if self.instance.objects.filter(user=request.user.id, recipe=pk).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('alredy_in_cart')}
            )
        self.instance.objects.create(user=request.user.id, recipe=pk)
        return RecipesInrerface().get_short_recipe(pk=pk)

    def delete_from_shoping_cart(self, request: request, pk: int = None) -> bool:
        if not self.instance.objects.filter(user=request.user.id, recipe=pk).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('not_in_cart')}
            )
        self.instance.objects.get(user=request.user.id, recipe=pk).delete()
        return True

    def download_shoping_cart(self, request: request) -> dict:
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
