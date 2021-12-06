from rest_framework.permissions import BasePermission


class IsOwnerUpateOrDelete(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' or request.method == 'PUT' or request.method == 'PATCH':
            """
            view.action своего рода костыль, так как при запросе из других приложений
            не корректно обрабатывается метод delete, так как пропадает разрешение
            на возможность убирать рецепт из избраного и корзины.
            данное поведение происходит из-за того что запрос приходит из другого приложения
            по внутреннему апи приложения т.е. вызывая REST API метод на удалении рецепта
            из корзины либо избранного отсутствует возможность дать понять что не только автор
            данного рецепта может удалять его из соответсвующего списка.
            По хорошему стоило разделить на второй фильтр, но применено yagni :)
            """
            if view.action == 'short_serializer':
                return True
            return obj.author == request.user.id
        return True
