from django.contrib import admin

from .models import ShopingCart


@admin.register(ShopingCart)
class ShopingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
