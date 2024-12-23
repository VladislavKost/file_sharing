from django.urls import path

from .views import FilesStoreView

urlpatterns = [
    path("", FilesStoreView.as_view(), name="create_file"),
]
