from django.core import validators
from django.db import models


class Recipe(models.Model):
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
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return f'id = {self.id} | название рецепта = {self.name}'


class IngredientsList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.PositiveBigIntegerField(
        verbose_name='Ингредиенты',
        validators=[validators.MinValueValidator(1)]
    )
    amount = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Список ингредиентов'
        verbose_name_plural = 'Список ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'], name='unique ingredient'
            )
        ]


class TagsList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='tags',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.PositiveBigIntegerField(
        verbose_name='Тег',
        validators=[validators.MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Список тегов'
        verbose_name_plural = 'Список тегов'
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'], name='unique tag'
            )
        ]
