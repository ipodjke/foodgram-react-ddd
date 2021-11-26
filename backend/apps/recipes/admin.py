from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model

from ingredients.models import Ingredient
from tags.models import Tag

from .models import IngredientsList, Recipe, TagsList


class RecipeAdminForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=get_user_model().objects.all(), label='Автор')

    def clean_author(self):
        return self.cleaned_data['author'].id


class IngredientsInlineForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), label='Ингредиент')

    def clean_ingredient(self):
        return self.cleaned_data['ingredient'].id


class IngredientsInline(admin.TabularInline):
    model = IngredientsList
    extra = 1
    form = IngredientsInlineForm


class TagsInlineForm(forms.ModelForm):
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), label='Тег')

    def clean_tag(self):
        return self.cleaned_data['tag'].id


class TagsInline(admin.TabularInline):
    model = TagsList
    extra = 1
    form = TagsInlineForm


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    inlines = [
        IngredientsInline,
        TagsInline
    ]
