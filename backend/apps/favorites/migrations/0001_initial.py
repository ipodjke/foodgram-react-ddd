# Generated by Django 3.1.13 on 2021-11-16 19:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Поьзователь')),
                ('recipe', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique recipe'),
        ),
    ]
