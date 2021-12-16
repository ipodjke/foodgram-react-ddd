import logging

from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.http import request

import users.interfaces as interface
from .serializers import (CreateUserSerializer, SetPasswordSerializer,
                          UserSerializer)
from utils.base_services import BaseService

User = get_user_model()

logger = logging.getLogger(__name__)


class UsersService(BaseService):
    instance = User
    serializer_class = UserSerializer

    # REST API logic
    def get_profile(self) -> dict:
        logger.info('Метод UsersService get_profile вызван')
        return self.retrieve(pk=self.request.user.id)

    def set_password(self) -> bool:
        logger.info('Метод UsersService set_password вызван')
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data['new_password'])
        self.request.user.save()
        return True

    # APP API logic
    def get_user(self, request: request, pk: int) -> dict:
        logger.info('Метод UsersService get_user вызван')
        self.__setattr__('request', request)
        return self.retrieve(pk=pk)

    # Interface logic
    def check_is_subscribed(self, context: dict, author: User) -> bool:
        logger.info('Метод UsersService check_is_subscribed вызван')
        request = context.get('request')
        if request is None or request.user.is_anonymous:
            return False

        return interface.SubscriptionsInterface().check_is_subscribed(user=request.user.id,
                                                                      author=author.id)

    # Service logic
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        elif self.action == 'set_password':
            return SetPasswordSerializer
        return super().get_serializer_class()


class UsersAdminService:
    instance = User

    def get_users(self) -> QuerySet:
        logger.info('Метод UsersService get_users вызван')
        return self.instance.objects.all()

    def get_user(self, pk: int) -> QuerySet:
        logger.info('Метод UsersService get_user_queryset вызван')
        return self.instance.objects.get(pk=pk)
