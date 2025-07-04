from .views import LoginAPIView, RegisterAPIView, LogoutAPIView, WhoAmiAPIView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name = 'login'),
    path('register/', RegisterAPIView.as_view(), name = 'register'),
    path('logout/', LogoutAPIView.as_view(), name = 'logout'),
    path('whoami/', WhoAmiAPIView.as_view(), name = 'whoami'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]