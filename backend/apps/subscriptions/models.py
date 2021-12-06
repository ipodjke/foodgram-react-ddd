from django.core.validators import MinValueValidator
from django.db import models


class Subscriptions(models.Model):
    follower = models.BigIntegerField(
        verbose_name='Подписчик',
        validators=[MinValueValidator(1)]
    )
    author = models.BigIntegerField(
        verbose_name='Автор',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'author'], name='unique subscription'
            )
        ]

    def __str__(self) -> str:
        return f'id = {self.id} | follower = {self.follower} | author = {self.author}'
