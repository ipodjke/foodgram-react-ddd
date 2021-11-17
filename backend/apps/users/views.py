from django.conf import settings as django_settings
from django.contrib.auth import get_user_model

from djoser.conf import settings
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.generalizing_functions import (check_the_occurrence,
                                          send_bad_request_response)
from utils.mixins import DisableUslessDjoserActionMixin

User = get_user_model()


class UserViewSet(DisableUslessDjoserActionMixin, DjoserUserViewSet):
    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = settings.PERMISSIONS.user_detail
        return super().get_permissions()

    def get_serializer_class(self):
        if (self.action == 'list_subscriptions'
                or self.action == 'subscribe_on_user'):
            return settings.SERIALIZERS.user_subscriptions
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action == 'list_subscriptions':
            return self.request.user.subscriptions.all()
        return super().get_queryset()

    @action(detail=False, url_path='subscriptions',
            permission_classes=[IsAuthenticated])
    def list_subscriptions(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True, url_path='subscribe',
            permission_classes=[IsAuthenticated])
    def subscribe_on_user(self, request, id=None, *args, **kwargs):
        author = self.get_object()
        user = request.user

        if author == user:
            return send_bad_request_response(
                django_settings.ERROR_MESSAGE.get('self_subscription')
            )

        if check_the_occurrence(author, 'subscriptions', user):
            return send_bad_request_response(
                django_settings.ERROR_MESSAGE.get('alredy_subscribe')
            )

        user.subscriptions.add(author.id)
        return self.retrieve(request, id=None, *args, **kwargs)

    @subscribe_on_user.mapping.delete
    def unsubscribe_on_user(self, request, id=None, *args, **kwargs):
        author = self.get_object()
        user = request.user

        if not check_the_occurrence(author, 'subscriptions', user):
            return send_bad_request_response(
                django_settings.ERROR_MESSAGE.get('not_subscribe')
            )

        user.subscriptions.remove(author.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
