import logging

from django.contrib.auth import get_user_model
from django.http import request

import users.interfaces as interface
from utils.base_services import BaseService

from .serializers import (CreateUserSerializer, SetPasswordSerializer,
                          UserSerializer)

logger = logging.getLogger(__name__)

User = get_user_model()


class UsersService(BaseService):
    instance = User
    serializer_class = UserSerializer
    logger = logging.getLogger(__name__)

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
