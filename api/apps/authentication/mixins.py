from rest_framework import permissions

from api.apps.authentication.auth import ClientJWTAuthentication


class ClientMixin:
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [ClientJWTAuthentication]
    pagination_class = None

    def get_client_id(self):
        return self.request.auth.get("client_id")

    def get_queryset(self):
        return self.queryset.filter(client=self.get_client_id()).order_by("id")

    def perform_create(self, serializer):
        serializer.save(client_id=self.get_client_id())

    def perform_update(self, serializer):
        serializer.save(client_id=self.get_client_id())
