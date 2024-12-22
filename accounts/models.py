from django.db import models
from django.contrib.auth.models import AbstractUser


def profile_directory_path(instance, filename):
    return "profile_user_images/user_{0}/{1}".format(instance.id, filename)


class CustomUser(AbstractUser):
    user_image = models.ImageField(
        upload_to=profile_directory_path, blank=True, null=True
    )
    gender = models.CharField(
        choices=[("male", "Male"), ("female", "Female")], null=True
    )
