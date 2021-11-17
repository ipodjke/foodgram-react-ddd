from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.name} | {self.measurement_unit}'
