# authentication.py
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class ClientJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        user_auth_tuple = super().authenticate(request)
        if user_auth_tuple is None:
            return None

        user, token = user_auth_tuple
        token_client_id = token.get("client_id")

        if not user.clients.filter(id=token_client_id).exists():
            raise AuthenticationFailed("Invalid client.")

        return user, token
