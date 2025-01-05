from django.urls import path

from .views import FilesStoreView, FileStoreView

urlpatterns = [
    path("", FilesStoreView.as_view(), name="create_file"),
    path("<str:id>/", FileStoreView.as_view(), name="get_file"),
]
