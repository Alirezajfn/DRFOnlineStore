from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from permissions.models import PermissionPerUrls, Role
from users.managers import CustomUserManager


class CustomPermissionMixin(models.Model):
    """
    This mixin is used to add the fields of permissions and groups to the user model
    """
    permissions_per_url = models.ManyToManyField(
        PermissionPerUrls,
        verbose_name=_("user permissions per url"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
    )

    role = models.ManyToManyField(
        Role,
        verbose_name=_("roles"),
        blank=True,
        help_text=_("Specific roles for this user."),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True


class User(AbstractUser, CustomPermissionMixin):
    objects = CustomUserManager()
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email']

    class Meta:
        indexes = [
            models.Index(fields=['email', ]),
        ]
