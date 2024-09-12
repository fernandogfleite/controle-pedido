from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "v1/",
        include(
            [
                path("auth/", include("api.apps.authentication.urls")),
                path("order/", include("api.apps.order.urls")),
            ]
        ),
    ),
]
