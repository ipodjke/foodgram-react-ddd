from django.core.validators import MinValueValidator
from django.db import models


class Favorite(models.Model):
    user = models.BigIntegerField(
        verbose_name='Пользователь',
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

    def __str__(self) -> str:
        return f'id = {self.id} | user = {self.user} | recipe = {self.recipe}'
