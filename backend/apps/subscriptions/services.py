import logging
from collections import OrderedDict
from re import A

from django.conf import settings
from django.http import request

import subscriptions.services as service
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from recipes.interfaces import UsersInterface
from utils.base_services import BaseService

from .interfaces import RecipesInrerface, UserInterface
from .models import Subscriptions
from .serializers import SubscriptionsSerializer

logger = logging.getLogger(__name__)


class SubscriptionsService(BaseService):
    def __init__(self):
        self.instance = Subscriptions
        self.pagination_class = api_settings.DEFAULT_PAGINATION_CLASS()

    def get_list_subs(self, request: request) -> dict:
        queryset = self.instance.objects.filter(follower=request.user.id)
        page = self.pagination_class.paginate_queryset(queryset=queryset, request=request, view=None)
        users = [UserInterface().get_user(pk=obj.author) for obj in page]
        context = {'limit': request.query_params.get('recipes_limit')}
        serializer = SubscriptionsSerializer(users, many=True, context=context)

        return OrderedDict([
            ('count', self.pagination_class.page.paginator.count),
            ('next', self.pagination_class.get_next_link()),
            ('previous', self.pagination_class.get_previous_link()),
            ('result', serializer.data)
        ])

    def subscribe(self, request: request, pk: int = None) -> dict:
        if request.user.id == pk:
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('self_subscription')}
            )
        if self.instance.objects.filter(follower=request.user.id, author=pk).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('alredy_subscribe')}
            )

        self.instance.objects.create(follower=request.user.id, author=pk)
        author = UsersInterface().get_user(pk=pk)
        context = {'limit': request.query_params.get('recipes_limit')}
        serializer = SubscriptionsSerializer(author, context=context)

        return serializer.data

    def unsubscribe(self, request: request, pk: int = None) -> bool:
        if request.user.id == pk:
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('self_unsubscription')}
            )
        if not self.instance.objects.filter(follower=request.user.id, author=pk).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('not_subscribe')}
            )
        self.instance.objects.get(follower=request.user.id, author=pk).delete()
        return True

    def get_recipes(self, author: int) -> dict:
        return RecipesInrerface().get_author_recipes(author=author)

    def get_count_recipes(self, author: int) -> dict:
        return RecipesInrerface().get_count_author_recipes(author=author)
