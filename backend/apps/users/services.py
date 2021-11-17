import logging
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.db import models
from django.http import request
from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings

from utils.base_services import BaseService

from .serializers import (CreateUserSerializer, SetPasswordSerializer,
                          UserSerializer)

logger = logging.getLogger(__name__)

User = get_user_model()


class UsersService(BaseService):
    def __init__(self):
        self.instance = User
        self.pagination_class = api_settings.DEFAULT_PAGINATION_CLASS()

    def get_by_id(self, instance_id: int) -> models.Model:
        logger.info('Get user by id.')
        queryset = super().get_by_id(instance_id)
        serializer = UserSerializer(queryset)
        return serializer.data

    def get_pagination_list(self, request) -> dict:
        logger.info('Get pagination users list.')
        queryset = self.instance.objects.all()
        page = self.pagination_class.paginate_queryset(queryset=queryset, request=request, view=None)

        if page is not None:
            serializer = UserSerializer(page, many=True)
            return OrderedDict([
                ('count', self.pagination_class.page.paginator.count),
                ('next', self.pagination_class.get_next_link()),
                ('previous', self.pagination_class.get_previous_link()),
                ('result', serializer.data)
            ])

        serializer = UserSerializer(queryset, many=True)
        return serializer.data

    def create_user(self, request: request) -> dict:
        logger.info('Create user.')
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get_profile(self, request: request) -> dict:
        logger.info('Get user profile.')
        return self.get_by_id(request.user.id)

    def set_password(self, request: request) -> bool:
        logger.info('Change user password.')
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.data['new_password'])
        request.user.save()

        return True
