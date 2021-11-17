import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import UsersService

logger = logging.getLogger(__name__)


class UsersAPI(viewsets.ViewSet):

    service = UsersService()

    def list(self, request: object) -> HttpResponse:
        logger.info('Метод UsersApi list вызван')
        return Response(self.service.get_pagination_list(request))

    def retrieve(self, request: request = None, pk: int = None) -> HttpResponse:
        logger.info('Метод UsersApi retrieve вызван')
        return Response(self.service.get_by_id(request=request, pk=pk))

    def create(self, request: request) -> HttpResponse:
        logger.info('Метод UsersApi create вызван')
        return Response(self.service.create_user(request))

    @action(detail=False, url_path='me', permission_classes=[IsAuthenticated])
    def get_user_profile(self, request: request) -> HttpResponse:
        logger.info('Метод UsersApi get_user_profile вызван')
        return Response(self.service.get_profile(request))

    @action(detail=False, url_path='set_password', permission_classes=[IsAuthenticated])
    def set_password(self, request: request) -> HttpResponse:
        logger.info('Метод UsersApi set_password вызван')
        if self.service.set_password(request):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
