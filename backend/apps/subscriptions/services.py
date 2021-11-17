import logging
from collections import OrderedDict

from django.conf import settings
from django.http import request

from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

import subscriptions.interfaces as interface
from recipes.interfaces import UsersInterface
from utils.base_services import BaseService

from .models import Subscriptions
from .serializers import SubscriptionsSerializer

logger = logging.getLogger(__name__)


class SubscriptionsService(BaseService):
    def __init__(self):
        self.instance = Subscriptions
        self.pagination_class = api_settings.DEFAULT_PAGINATION_CLASS()

    def get_list_subs(self, request: request) -> dict:
        logger.info('Метод SubscriptionsService get_list_subs вызван')
        queryset = self.instance.objects.filter(follower=request.user.id)

        page = self.pagination_class.paginate_queryset(
            queryset=queryset,
            request=request,
            view=None
        )

        users = [interface.UserInterface().get_user(pk=obj.author) for obj in page]
        context = {'limit': request.query_params.get('recipes_limit')}
        serializer = SubscriptionsSerializer(users, many=True, context=context)

        return OrderedDict([
            ('count', self.pagination_class.page.paginator.count),
            ('next', self.pagination_class.get_next_link()),
            ('previous', self.pagination_class.get_previous_link()),
            ('result', serializer.data)
        ])

    def subscribe(self, request: request, pk: int = None) -> dict:
        logger.info('Метод SubscriptionsService subscribe вызван')
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
        logger.info('Метод SubscriptionsService unsubscribe вызван')
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
        logger.info('Метод SubscriptionsService get_recipes вызван')
        return interface.RecipesInrerface().get_author_recipes(author=author)

    def get_count_recipes(self, author: int) -> dict:
        logger.info('Метод SubscriptionsService get_count_recipes вызван')
        return interface.RecipesInrerface().get_count_author_recipes(author=author)

    def check_is_subscribed(self, user: int, author: int) -> dict:
        logger.info('Метод SubscriptionsService check_is_subscribed вызван')
        return self.instance.objects.filter(follower=user, author=author).exists()
