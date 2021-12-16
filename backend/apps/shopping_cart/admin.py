from django.contrib import admin

import shopping_cart.services as service
from .forms import ShoppingCartAdminForm
from .models import ShoppingCart


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
