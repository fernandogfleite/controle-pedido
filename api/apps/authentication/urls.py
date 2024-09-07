from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.apps.authentication.serializers.jwt import MyTokenObtainPairSerializer

app_name = "authentication"

urlpatterns = [
    path(
        "token/",
        TokenObtainPairView.as_view(serializer_class=MyTokenObtainPairSerializer),
        name="token_obtain_pair",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
