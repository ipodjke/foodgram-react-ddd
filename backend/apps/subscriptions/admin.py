from django.contrib import admin

import subscriptions.services as service
from .forms import SubscriptionsAdminForm
from .models import Subscription


@admin.register(Subscription)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('get_follower', 'get_author')
    form = SubscriptionsAdminForm

    def get_follower(self, obj):
        return service.SubscriptionsAdminService().get_user(pk=obj.follower)
    get_follower.short_description = 'Подписчик'

    def get_author(self, obj):
        return service.SubscriptionsAdminService().get_user(pk=obj.author)
    get_author.short_description = 'Автор'
