from django.db import models
from accounts.models import CustomUser


def users_file_directory_path(instance, filename):
    return "users_files/user_{0}/{1}".format(instance.owner_id.id, filename)


class FileStore(models.Model):
    file = models.FileField(
        upload_to=users_file_directory_path,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    unique_code = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    last_downloaded = models.DateTimeField(blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
