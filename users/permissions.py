from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Проверяет является ли пользователь модератором.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет является ли пользователь владельцем.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
