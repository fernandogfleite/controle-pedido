from rest_framework import serializers

from api.apps.authentication.models.client import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
        )
