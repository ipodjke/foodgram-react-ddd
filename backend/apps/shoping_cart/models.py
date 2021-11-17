from django.core.validators import MinValueValidator
from django.db import models


class ShopingCart(models.Model):
    user = models.BigIntegerField(
        verbose_name='Поьзователь',
        validators=[MinValueValidator(1)]
    )
    recipe = models.BigIntegerField(
        verbose_name='Рецепт',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique shoping recipe'
            )
        ]
