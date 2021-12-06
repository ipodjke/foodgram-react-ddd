from django import forms
from django.contrib import admin

import subscriptions.services as service
from shopping_cart import services

from .models import Subscriptions


class ShoppingCartAdminForm(forms.ModelForm):
    follower = forms.ModelChoiceField(
        queryset=service.SubscriptionsAdminService().get_users(),
        label='Подписчик'
    )
    author = forms.ModelChoiceField(
        queryset=service.SubscriptionsAdminService().get_users(),
        label='Автор'
    )

    def clean_follower(self):
        return self.cleaned_data['follower'].id

    def clean_author(self):
        return self.cleaned_data['author'].id

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['follower'] == cleaned_data['author']:
            msg = 'Нельзя подписаться на самого себя'
            self.add_error('follower', msg)
            self.add_error('author', msg)


@admin.register(Subscriptions)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('get_follower', 'get_author')
    form = ShoppingCartAdminForm

    def get_follower(self, obj):
        return services.ShoppingCartAdminService().get_user(pk=obj.follower)
    get_follower.short_description = 'Подписчик'

    def get_author(self, obj):
        return services.ShoppingCartAdminService().get_user(pk=obj.author)
    get_author.short_description = 'Автор'
