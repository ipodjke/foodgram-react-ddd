from django import forms

import favorites.services as service


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
