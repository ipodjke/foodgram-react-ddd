from django.contrib import admin

from .models import IngredientsList, Recipe, TagsList


@admin.register(Recipe)
class RecipeNewAdmin(admin.ModelAdmin):
    pass


@admin.register(IngredientsList)
class IngredientsListNewAdmin(admin.ModelAdmin):
    pass


@admin.register(TagsList)
class TagsListNewAdmin(admin.ModelAdmin):
    pass
