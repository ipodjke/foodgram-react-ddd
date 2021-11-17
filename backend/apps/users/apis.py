import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import UsersService

logger = logging.getLogger(__name__)


class UsersAPI(viewsets.ViewSet):

    user_service = UsersService()

    def list(self, request: object) -> HttpResponse:
        logger.info('Метод UsersApi list вызван')
        return Response(self.user_service.get_pagination_list(request))

    def retrieve(self, request: request = None, pk: int = None) -> HttpResponse:
        logger.info('Метод UsersApi retrieve вызван')
        return Response(self.user_service.get_by_id(instance_id=pk))

    def create(self, request: request) -> HttpResponse:
        logger.info('Метод UsersApi create вызван')
        return Response(self.user_service.create_user(request))

    @action(detail=False, url_path='me_new', permission_classes=[IsAuthenticated])
    def get_user_profile(self, request: request) -> HttpResponse:
        return Response(self.user_service.get_profile(request))

    @action(detail=False, url_path='set_password_new', permission_classes=[IsAuthenticated])
    def set_password(self, request: request) -> HttpResponse:
        if self.user_service.set_password(request):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
