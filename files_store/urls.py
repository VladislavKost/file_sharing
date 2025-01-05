from django.urls import path

from .views import FilesStoreView, FileStoreView, FilesStoreAllView

urlpatterns = [
    path("", FilesStoreView.as_view(), name="create_file"),
    path("all/", FilesStoreAllView.as_view(), name="all_files"),
    path("<str:id>/", FileStoreView.as_view(), name="get_file"),
]
