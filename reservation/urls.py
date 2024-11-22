from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("admin/", admin.site.urls),
]


urlpatterns += i18n_patterns(
    path("", include("reservation.apps.authentication.urls")),
    path("silk/", include("silk.urls", namespace="silk")),
)

urlpatterns += [
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # Obtenir un token JWT
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Rafraîchir un token JWT
    path(
        "api/v1/", include("reservation.apps.api.V.v1.urls")
    ),  # Inclut les routes de ton API
]
