from django import forms
from django.contrib import admin

import recipes.services as service

from .models import IngredientsList, Recipe, TagsList


class RecipeAdminForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=service.RecipesAdminService().get_users(),
        label='Автор'
    )

    def clean_author(self):
        return self.cleaned_data['author'].id


class IngredientsInlineForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=service.RecipesAdminService().get_ingredients(),
        label='Ингредиент'
    )

    def clean_ingredient(self):
        return self.cleaned_data['ingredient'].id


class IngredientsInline(admin.TabularInline):
    model = IngredientsList
    extra = 1
    form = IngredientsInlineForm


class TagsInlineForm(forms.ModelForm):
    tag = forms.ModelChoiceField(
        queryset=service.RecipesAdminService().get_tags(),
        label='Тег'
    )

    def clean_tag(self):
        return self.cleaned_data['tag'].id


class TagsInline(admin.TabularInline):
    model = TagsList
    extra = 1
    form = TagsInlineForm


class CustomAuthorAdminFilter(admin.SimpleListFilter):
    """ Фильтр для отоброжения человекочитаемых имен автора.

    Основное прдназначение уйти от отображения не понятных id авторов
    к их именам.
    В связи с тем, что используем DDD в модели храниться id автора, а не
    ссылка на него, в связи с этим стандартное поведение джано admin отображает
    его id, по этой причине и что бы осуществить понятное использование
    фильтрации был создан данный фильтр.
    В lookups запрашиваем все объекты user и создаем список кортежй (id, login)
    В qeuryset фильтрацию по id
    """
    title = 'Автор'
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        users = service.RecipesAdminService().get_users()
        return [(user.id, user.email) for user in users]

    def queryset(self, request, queryset):
        return queryset.filter(author=self.value()) if self.value() else queryset


class CustomTagAdminFilter(admin.SimpleListFilter):
    """ Фильтр для отоброжения человекочитаемых имен тегов.

    Основное прдназначение уйти от отображения списка не понятных объектов модели Тегов
    к списку имен тегов без их повторений.
    В связи с тем, что используем DDD в модели храниться связб на модель тегов которая содержит
    связь рецепта и его тегов, в свою очередь теги являются id Tags, а не
    ссылка на него, в связи с этим стандартное поведение джано admin отображает
    объекты вспомогательной модели TagsList, по этой причине и что бы осуществить понятное
    использование фильтрации был создан данный фильтр.
    В lookups запрашиваем все объекты Tags и создаем список кортежй (id, name)
    В qeuryset фильтрацию по id
    """
    title = 'Тег'
    parameter_name = 'tags'

    def lookups(self, request, model_admin):
        tags = service.RecipesAdminService().get_tags()
        return [(tag.id, tag.name) for tag in tags]

    def queryset(self, request, queryset):
        return queryset.filter(tags__tag=self.value()) if self.value() else queryset


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    inlines = [
        IngredientsInline,
        TagsInline
    ]
    list_display = ('name', 'get_author', 'total_number_of_additions')
    list_filter = ('name', CustomAuthorAdminFilter, CustomTagAdminFilter)

    def get_author(self, obj):
        return service.RecipesAdminService().get_user(pk=obj.author)
    get_author.short_description = 'Автор'

    def total_number_of_additions(self, obj):
        return service.RecipesAdminService().get_total_number_of_additions(pk=obj.id)
    total_number_of_additions.short_description = ('Общее количесвто '
                                                   'добавлений в избранное')
