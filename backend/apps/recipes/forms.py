from django import forms

import recipes.services as service


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


class TagsInlineForm(forms.ModelForm):
    tag = forms.ModelChoiceField(
        queryset=service.RecipesAdminService().get_tags(),
        label='Тег'
    )

    def clean_tag(self):
        return self.cleaned_data['tag'].id
