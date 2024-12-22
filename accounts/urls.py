from django.urls import path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
)

from .views import CustomUserView, CustomLoginView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="rest_login"),
    path("profile/", CustomUserView.as_view(), name="user_profile"),
]
