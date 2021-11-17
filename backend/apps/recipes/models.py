from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Картинка рецепта'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes_tags',
        blank=True,
        verbose_name='Теги рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsList',
        verbose_name='Ингредиенты'
    )
    publication_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ('-publication_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return (f'{self.id} | {self.name} | '
                f'{self.tags.all()[:5]} |{self.ingredients.all()[:5]}')


class IngredientsList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='through_recipe',
        on_delete=models.CASCADE
    )
    ingredients = models.ForeignKey(
        Ingredient,
        related_name='through_ingredients',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField()


class MarkedUserRecipes(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='marked_recipes',
        verbose_name='Пользователь',
    )
    fovorited_recipe = models.ManyToManyField(
        Recipe,
        related_name='marked_favorited_recipes',
        blank=True,
        verbose_name='Понравившиеся рецепты',
    )
    recipe_for_download = models.ManyToManyField(
        Recipe,
        related_name='marked_download_recipes',
        blank=True,
        verbose_name='Рецепты для скачивания'
    )

    class Meta:
        verbose_name = 'Отмеченый рецепт'
        verbose_name_plural = 'Отмеченные рецепты'

    def __str__(self) -> str:
        return (f'{self.id} | {self.user} | '
                f'{self.recipe_for_download.all()[:5]} | '
                f'{self.fovorited_recipe.all()[:5]}')


class RecipeNew(models.Model):
    author = models.PositiveBigIntegerField(
        verbose_name='Автор рецепта',
        validators=[validators.MinValueValidator(1)]
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Картинка рецепта'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
    publication_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ('-publication_date',)
        verbose_name = 'Рецепт_new'
        verbose_name_plural = 'Рецепты_new'

    def __str__(self) -> str:
        return (f'{self.id} | {self.name} | '
                f'{self.tags.all()[:5]} |{self.ingredients.all()[:5]}')


class IngredientsListNew(models.Model):
    recipe = models.ForeignKey(
        RecipeNew,
        related_name='ingredients',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.PositiveBigIntegerField(
        verbose_name='Ингредиенты',
        validators=[validators.MinValueValidator(1)]
    )
    amount = models.PositiveSmallIntegerField()


class TagsListNew(models.Model):
    recipe = models.ForeignKey(
        RecipeNew,
        related_name='tags',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.PositiveBigIntegerField(
        verbose_name='Тег',
        validators=[validators.MinValueValidator(1)]
    )
