from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


class User(AbstractUser):
    objects = CustomUserManager()
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email']

    class Meta:
        indexes = [
            models.Index(fields=['email', ]),
        ]

