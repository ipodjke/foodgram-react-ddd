import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import SubscriptionsService

logger = logging.getLogger(__name__)


class SubscriptionsAPI(viewsets.ViewSet):

    service = SubscriptionsService()

    @action(detail=False, url_path='subscriptions', permission_classes=[IsAuthenticated])
    def get_subscriptions(self, request: request) -> HttpResponse:
        logger.info('Метод SubscriptionsAPI get_subscriptions вызван')
        return Response(self.service.get_list_subs(request))

    @action(detail=True, url_path='subscribe', permission_classes=[IsAuthenticated])
    def subscribe_on_user(self, request: request, pk: str = None) -> HttpResponse:
        logger.info('Метод SubscriptionsAPI subscribe_on_user вызван')
        return Response(self.service.subscribe(request=request, pk=int(pk)))

    @subscribe_on_user.mapping.delete
    def unsubscribe_on_user(self, request: request, pk: str = None) -> HttpResponse:
        logger.info('Метод SubscriptionsAPI unsubscribe_on_user вызван')
        self.service.unsubscribe(request=request, pk=int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def check_is_subscribed(self, user: int, author: int) -> HttpResponse:
        logger.info('Метод SubscriptionsAPI check_is_subscribed вызван')
        return Response(self.service.check_is_subscribed(user=user, author=author))
