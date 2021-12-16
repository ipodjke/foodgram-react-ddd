from django.contrib import admin

import favorites.services as service
from .forms import FavoritesAdminForm
from .models import Favorite


@admin.register(Favorite)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_recipe')
    form = FavoritesAdminForm

    def get_recipe(self, obj):
        return service.FavoritesAdminService().get_recipe(pk=obj.recipe)
    get_recipe.short_description = 'Рецепт'

    def get_user(self, obj):
        return service.FavoritesAdminService().get_user(pk=obj.user)
    get_user.short_description = 'Пользователь'
