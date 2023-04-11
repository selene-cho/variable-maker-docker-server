from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    사용자를 나타내는 모델
    """

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    name = models.CharField(
        max_length=150,
        default="",
    )
