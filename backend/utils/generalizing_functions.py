from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response


def check_the_occurrence(ckecked_obj: object,
                         related_field: str,
                         obj: object) -> bool:
    """
    Проверить вхождение объекта.

    Функция проверяет объекты находятся ли они
    в различных списках избранного пользователя.

    ------
    Note!!!!!:
        Функция используется только совместно с SerializerMethodField
        related_field допускает использование __ снитаксиса для доступа
            к другим сылочным полям.
        Ловит исключение если передано не корректное related_field
    ------
    Параметры:
        obj - обьект в котором будет произведен поиск на наличие объекта
        ckecked_obj - Проверяемый на вхождение объект
        related_field - поле в котором находятся подписки и т.д.
    ------
    Выходное значение:
        bool - находится ли обьъект в списке или нет.
    """
    try:
        user = obj.context.get('request').user
    except AttributeError:
        user = obj

    try:
        if user.is_anonymous:
            return False
    except AttributeError:
        pass

    requested_field = user
    try:
        for field in related_field.split('__'):
            requested_field = getattr(requested_field, field)
    except AttributeError:
        return False

    data = getattr(requested_field, 'all')()

    if ckecked_obj in data:
        return True
    return False


def send_bad_request_response(message: str) -> object:
    return Response(
        {'errors': message},
        status=status.HTTP_400_BAD_REQUEST
    )
