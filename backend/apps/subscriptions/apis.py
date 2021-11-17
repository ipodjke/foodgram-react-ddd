import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import SubscriptionsService

logger = logging.getLogger(__name__)


class SubscriptionsAPI(viewsets.ViewSet):

    subscriptions_service = SubscriptionsService()

    @action(detail=False, url_path='subscriptions_new', permission_classes=[IsAuthenticated])
    def get_subscriptions(self, request: request) -> HttpResponse:
        return Response(self.subscriptions_service.get_list_subs(request))

    @action(detail=True, url_path='subscribe_new', permission_classes=[IsAuthenticated])
    def subscribe_on_user(self, request: request, pk: str = None) -> HttpResponse:
        return Response(self.subscriptions_service.subscribe(request=request, pk=int(pk)))

    @subscribe_on_user.mapping.delete
    def unsubscribe_on_user(self, request: request, pk: str = None) -> HttpResponse:
        self.subscriptions_service.unsubscribe(request=request, pk=int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)
