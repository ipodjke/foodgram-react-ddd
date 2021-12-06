# Generated by Django 3.1.13 on 2021-12-04 03:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Пользователь')),
                ('recipe', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique shopping recipe'),
        ),
    ]
