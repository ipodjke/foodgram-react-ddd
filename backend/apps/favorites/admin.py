from django import forms
from django.contrib import admin

import favorites.services as service

from .models import Favorites


class FavoritesAdminForm(forms.ModelForm):
    recipe = forms.ModelChoiceField(
        queryset=service.FavoritesAdminService().get_recipes(),
        label='Рецепт'
    )
    user = forms.ModelChoiceField(
        queryset=service.FavoritesAdminService().get_users(),
        label='Пользователь'
    )

    def clean_recipe(self):
        return self.cleaned_data['recipe'].id

    def clean_user(self):
        return self.cleaned_data['user'].id


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_recipe')
    form = FavoritesAdminForm

    def get_recipe(self, obj):
        return service.FavoritesAdminService().get_recipe(pk=obj.recipe)
    get_recipe.short_description = 'Рецепт'

    def get_user(self, obj):
        return service.FavoritesAdminService().get_user(pk=obj.user)
    get_user.short_description = 'Пользователь'
