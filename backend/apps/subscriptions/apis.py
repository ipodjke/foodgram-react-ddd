import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import subscriptions.services as service

logger = logging.getLogger(__name__)


class SubscriptionsRestAPI(viewsets.ViewSet):
    @action(detail=False, url_path='subscriptions', permission_classes=[IsAuthenticated])
    def get_subscriptions(self, request: request) -> HttpResponse:
        logger.info('Метод SubscriptionsRestAPI get_subscriptions вызван')
        return Response(service.SubscriptionsService(request, self.kwargs).list_subs())

    @action(detail=True, url_path='subscribe', permission_classes=[IsAuthenticated])
    def subscribe_on_user(self, request: request, pk: str) -> HttpResponse:
        logger.info('Метод SubscriptionsRestAPI subscribe_on_user вызван')
        return Response(service.SubscriptionsService(request, self.kwargs).subscribe(pk=int(pk)))

    @subscribe_on_user.mapping.delete
    def unsubscribe_on_user(self, request: request, pk: str) -> HttpResponse:
        logger.info('Метод SubscriptionsRestAPI unsubscribe_on_user вызван')
        if service.SubscriptionsService(request, self.kwargs).unsubscribe(pk=int(pk)):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SubscriptionsAppAPI(viewsets.ViewSet):
    def check_is_subscribed(self, user: int, author: int) -> bool:
        logger.info('Метод SubscriptionsRestAPI check_is_subscribed вызван')
        return service.SubscriptionsService().check_is_subscribed(user=user, author=author)
