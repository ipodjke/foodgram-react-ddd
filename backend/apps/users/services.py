import logging
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.db import models
from django.http import request

from rest_framework.settings import api_settings

import users.interfaces as interface
from utils.base_services import BaseService

from .serializers import (CreateUserSerializer, SetPasswordSerializer,
                          UserSerializer)

logger = logging.getLogger(__name__)

User = get_user_model()


class UsersService(BaseService):
    def __init__(self):
        self.instance = User
        self.pagination_class = api_settings.DEFAULT_PAGINATION_CLASS()

    def get_by_id(self, request: request, pk: int) -> models.Model:
        logger.info('Метод UsersService get_by_id вызван')
        queryset = super().get_by_id(pk)

        context = {
            'user': queryset if request is None else request.user
        }

        serializer = UserSerializer(queryset, context=context)
        return serializer.data

    def get_pagination_list(self, request) -> dict:
        logger.info('Метод UsersService get_pagination_list вызван')
        queryset = self.instance.objects.all()
        page = self.pagination_class.paginate_queryset(
            queryset=queryset,
            request=request,
            view=None
        )
        serializer = UserSerializer(page, many=True, context={'user': request.user})
        return OrderedDict([
            ('count', self.pagination_class.page.paginator.count),
            ('next', self.pagination_class.get_next_link()),
            ('previous', self.pagination_class.get_previous_link()),
            ('result', serializer.data)
        ])

    def create_user(self, request: request) -> dict:
        logger.info('Метод UsersService create_user вызван')
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get_profile(self, request: request) -> dict:
        logger.info('Метод UsersService get_profile вызван')
        return self.get_by_id(request=request, pk=request.user.id)

    def set_password(self, request: request) -> bool:
        logger.info('Метод UsersService set_password вызван')
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.data['new_password'])
        request.user.save()

        return True

    def check_is_subscribed(self, context: dict, author: User) -> bool:
        logger.info('Метод UsersService check_is_subscribed вызван')
        user = context.get('user')

        if user.is_anonymous:
            return False

        return interface.SubscriptionsInterface().check_is_subscribed(user=user.id,
                                                                      author=author.id)
