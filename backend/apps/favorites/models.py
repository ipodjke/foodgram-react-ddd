from django.core.validators import MinValueValidator
from django.db import models


class Favorites(models.Model):
    user = models.BigIntegerField(
        verbose_name='Поьзователь',
        validators=[MinValueValidator(1)]
    )
    recipe = models.BigIntegerField(
        verbose_name='Рецепт',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique recipe'
            )
        ]
