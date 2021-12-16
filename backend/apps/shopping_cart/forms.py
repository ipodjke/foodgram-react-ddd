from django import forms

import shopping_cart.services as service


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
