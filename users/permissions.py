from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь создателем объекта.
    """

    def has_object_permission(self, request, view, obj):

        if obj.owner == request.user:
            return True
        return False


class IsUser(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем аккаунта.
    """

    def has_object_permission(self, request, view, obj):

        if obj.email == request.user.email:
            return True
        return False
