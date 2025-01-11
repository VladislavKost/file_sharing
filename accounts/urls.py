from django.urls import path

from .views import CustomUserView, CustomLoginView, CustomUsersView
from dj_rest_auth.views import LogoutView

urlpatterns = [
    path("", CustomUsersView.as_view(), name="users"),
    path("login/", CustomLoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("profile/", CustomUserView.as_view(), name="user_profile"),
    path("<str:id>/", CustomUserView.as_view(), name="users_id"),
]
