from django import forms

import subscriptions.services as service


class SubscriptionsAdminForm(forms.ModelForm):
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
