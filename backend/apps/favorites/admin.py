from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model

from recipes.models import Recipe

from .models import Favorites


class FavoritesAdminForm(forms.ModelForm):
    recipe = forms.ModelChoiceField(queryset=Recipe.objects.all(), label='Рецепт')
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all(), label='Пользователь')

    def clean_recipe(self):
        return self.cleaned_data['recipe'].id

    def clean_user(self):
        return self.cleaned_data['user'].id


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_recipe')
    form = FavoritesAdminForm

    def get_recipe(self, obj):
        return Recipe.objects.get(pk=obj.recipe)
    get_recipe.short_description = 'Рецепт'

    def get_user(self, obj):
        return get_user_model().objects.get(pk=obj.user)
    get_user.short_description = 'Пользователь'
