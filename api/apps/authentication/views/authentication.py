from rest_framework import generics, mixins, permissions
from rest_framework.response import Response

from api.apps.authentication.mixins import ClientMixin
from api.apps.authentication.models.client import User
from api.apps.authentication.serializers.authentication import UserSerializer


class RetriveMeView(ClientMixin, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
