from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя'
        )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='Электронная почта'
    )

    subscriptions = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        verbose_name='Подписки пользователя'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return (f'id = {self.id} | email = {self.email} | имя = {self.first_name}'
                f'фамилия = {self.last_name}')
