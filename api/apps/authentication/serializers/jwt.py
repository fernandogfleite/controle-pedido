from django.contrib.auth.models import update_last_login
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    client_id = serializers.IntegerField()
    token_class = RefreshToken

    @classmethod
    def get_token(cls, user, client_id):
        token = super().get_token(user)
        token["client_id"] = client_id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        client_id = attrs["client_id"]

        if not self.user.clients.filter(id=client_id).exists():
            raise ValidationError("Invalid client.")

        refresh = self.get_token(self.user, client_id)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["client_id"] = client_id

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
