import logging
from typing import Optional

from django.conf import settings
from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError

import subscriptions.interfaces as interface
from .models import Subscription
from .serializers import SubscriptionsSerializer
from utils.base_services import BaseService

logger = logging.getLogger(__name__)


class SubscriptionsService(BaseService):
    instance = Subscription
    serializer_class = SubscriptionsSerializer

    # REST API logic
    def list_subs(self) -> dict:
        logger.info('Метод SubscriptionsService list_subs вызван')
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        users = [interface.UserInterface().get_user(pk=obj.author, request=self.request) for obj in page] # noqa

        if page is not None:
            serializer = self.get_serializer(users, many=True)
            return self.get_paginated_data(serializer.data)

        serializer = SubscriptionsSerializer(
            [interface.UserInterface().get_user(pk=obj.author, request=self.request) for obj in queryset], # noqa
            many=True,
        )

        return serializer.data

    def subscribe(self, pk: int = None) -> dict:
        logger.info('Метод SubscriptionsService subscribe вызван')
        author = interface.UserInterface().get_user(pk=pk, request=self.request)
        serializer = self.get_serializer(data=author)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        author['is_subscribed'] = True
        serializer.instance = author
        return serializer.data

    def unsubscribe(self, pk: int = None) -> bool:
        logger.info('Метод SubscriptionsService unsubscribe вызван')
        self._validate_unsubscribe_request(self.request.user.id, pk)
        self.instance.objects.get(follower=self.request.user.id, author=pk).delete()
        return True

    # APP API logic
    def check_is_subscribed(self, user: int, author: int) -> bool:
        logger.info('Метод SubscriptionsService check_is_subscribed вызван')
        context = {'follower': user, 'author': author}
        return self.check_is_in(context)

    # Interface logic
    def get_author_recipes(self, author: int) -> QuerySet:
        logger.info('Метод SubscriptionsService get_recipes вызван')
        return interface.RecipesInrerface().get_author_recipes(author=author)

    def get_count_author_recipes(self, author: int) -> int:
        logger.info('Метод SubscriptionsService get_count_recipes вызван')
        return interface.RecipesInrerface().get_count_author_recipes(author=author)

    # Service logic
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(follower=self.request.user.id)

    # local functions
    def _validate_unsubscribe_request(self, follower: int, author: int) -> Optional[Exception]:
        if follower == author:
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('self_unsubscription')}
            )
        if not self.instance.objects.filter(follower=follower, author=author).exists():
            raise ValidationError(
                {'errors': settings.ERROR_MESSAGE.get('not_subscribe')}
            )


class SubscriptionsAdminService:
    def get_user(self, pk: int) -> QuerySet:
        logger.info('Метод SubscriptionsAdminService get_user вызван')
        return interface.UsersAdminInterface().get_user(pk=pk)

    def get_users(self) -> QuerySet:
        logger.info('Метод SubscriptionsAdminService get_users вызван')
        return interface.UsersAdminInterface().get_users()
