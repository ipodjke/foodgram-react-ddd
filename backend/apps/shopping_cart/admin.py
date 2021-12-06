from django import forms
from django.contrib import admin

import shopping_cart.services as service

from .models import ShoppingCart


class ShoppingCartAdminForm(forms.ModelForm):
    recipe = forms.ModelChoiceField(
        queryset=service.ShoppingCartAdminService().get_recipes(),
        label='Рецепт'
    )
    user = forms.ModelChoiceField(
        queryset=service.ShoppingCartAdminService().get_users(),
        label='Пользователь'
    )

    def clean_recipe(self):
        return self.cleaned_data['recipe'].id

    def clean_user(self):
        return self.cleaned_data['user'].id


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_recipe')
    form = ShoppingCartAdminForm

    def get_recipe(self, obj):
        return service.ShoppingCartAdminService().get_recipe(pk=obj.recipe)
    get_recipe.short_description = 'Рецепт'

    def get_user(self, obj):
        return service.ShoppingCartAdminService().get_user(pk=obj.user)
    get_user.short_description = 'Пользователь'
