from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


class User(AbstractUser):
    objects = CustomUserManager()
    REQUIRED_FIELDS = []
    email = models.EmailField(unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['email', ]),
        ]

