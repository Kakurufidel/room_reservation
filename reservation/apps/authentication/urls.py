from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, LogoutView

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    #  path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/", obtain_auth_token, name="login"),
    path("logout/", LogoutView.as_view(), name="api_logout"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
