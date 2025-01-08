from django.urls import path

from .views import CustomUserView, CustomLoginView, CustomUsersView

urlpatterns = [
    path("", CustomUsersView.as_view(), name="users"),
    path("login/", CustomLoginView.as_view(), name="rest_login"),
    path("profile/", CustomUserView.as_view(), name="user_profile"),
    path("<str:id>/", CustomUserView.as_view(), name="users_id"),
]
