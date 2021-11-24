import logging

from django.http import request
from django.http.response import HttpResponse

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import UsersService

logger = logging.getLogger(__name__)


class UsersRestAPI(viewsets.ViewSet):
    service = UsersService

    def list(self, request: object) -> HttpResponse:
        logger.info('Метод UsersApi list вызван')
        return Response(self.service(request, self.kwargs).list())

    def retrieve(self, request: request, pk: int) -> HttpResponse:
        logger.info('Метод UsersApi retrieve вызван')
        return Response(self.service(request, self.kwargs).retrieve())

    def create(self, request: request) -> HttpResponse:
        logger.info('Метод UsersApi create вызван')
        return Response(self.service(request, self.kwargs, self.action).create())

    @action(detail=False, url_path='me', permission_classes=[IsAuthenticated])
    def get_user_profile(self, request: request) -> HttpResponse:
        logger.info('Метод UsersApi get_user_profile вызван')
        return Response(self.service(request).get_profile())

    @action(detail=False, url_path='set_password', methods=['POST'],
            permission_classes=[IsAuthenticated])
    def set_password(self, request: request) -> HttpResponse:
        logger.info('Метод UsersApi set_password вызван')
        if self.service(request, self.kwargs, self.action).set_password():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class UsersAppAPI:
    service = UsersService

    def get_user(self, request: request, pk: int) -> dict:
        logger.info('Метод UsersAppAPI get_user вызван')
        return self.service().get_user(pk=pk, request=request)
