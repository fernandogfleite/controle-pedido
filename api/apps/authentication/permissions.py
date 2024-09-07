from rest_framework import permissions
from rest_framework.request import Request


class IsClientUser(permissions.BasePermission):
    def has_permission(self, request, view):
        client_id = request.auth.get("client_id")

        return (
            request.user.is_authenticated
            and request.user.clients.filter(id=client_id).exists()
        )
