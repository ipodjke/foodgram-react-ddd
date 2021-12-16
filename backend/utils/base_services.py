from collections import OrderedDict

from django.db import models
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework import exceptions
from rest_framework.settings import api_settings

from .mixins import CreateMixin, DestroyMixin, ListMixin, RetrieveMixin


class BaseService(CreateMixin, DestroyMixin, ListMixin, RetrieveMixin):
    """
    Базовый сервис с бизенес логикой для всех приложений.
    """

    instance: models.Model = None
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    lookup_field = 'pk'
    lookup_url_kwarg = None
    permission_classes = []
    serializer_class = None
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    include_to_lookup = None

    def __init__(self, request=None, self_kwargs=None, action=None):
        self.action = action
        self.request = request
        self.kwargs = self_kwargs

        assert self.instance is not None, (
            f'Необходимо указать instance(модель) в {self.__class__.__name__}'
        )
        assert self.serializer_class is not None, (
            f'Необходимо указать serializer_class в {self.__class__.__name__}'
        )

    # секция получения объектов
    def get_queryset(self):
        return self.filter_queryset(self.instance.objects.all())

    def get_object(self, context: dict = None):
        queryset = self.instance.objects.all()
        if context is None:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            filter_kwargs = self.update_filter_kwargs(filter_kwargs, self.include_to_lookup)
        else:
            filter_kwargs = context

        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def check_is_in(self, context: dict = None):
        try:
            self.get_object(context)
            return True
        except Http404:
            return False

    # секция фильтрации
    def update_filter_kwargs(self, filter_kwargs, additional_kwargs):
        if additional_kwargs is None:
            return filter_kwargs
        for key, value in additional_kwargs.items():
            if isinstance(value, str):
                filter_kwargs[key] = eval(value)
                continue
            filter_kwargs[key] = value
        return filter_kwargs

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    # секция для работы с примишинами
    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def permission_denied(self, request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=message, code=code)

    # секция для работы с сериализаторами
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer_context(self):
        return {
            'request': self.request,
        }

    # секция для работы с пагинатором
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_data(self, data):
        return OrderedDict([
            ('count', self.paginator.page.paginator.count),
            ('next', self.paginator.get_next_link()),
            ('previous', self.paginator.get_previous_link()),
            ('results', data)
        ])
