from django.utils.itercompat import is_iterable
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from rest_framework.exceptions import PermissionDenied

from permissions.models import Permission
from users.managers import CustomUserManager


# def _user_has_perm_per_url(self, perm, obj):
#     """
#     A backend can raise `PermissionDenied` to short-circuit permission checking.
#     """
#     for backend in self._get_backends(return_tuples=True):
#         try:
#             if backend.has_perm_per_url(self, perm, obj):
#                 return True
#         except PermissionDenied:
#             return False
#     return False


# def _user_get_permissions_per_url(self, obj, param):
#     """
#     Return a set of permission strings the user has, including their
#     group permissions. This method queries all available auth backends.
#     If an object is passed in, only permissions matching this object
#     are returned.
#     """
#     permissions = set()
#     name = '{}_permissions_per_url'.format(param)
#     for backend in self._get_backends(return_tuples=True):
#         if hasattr(backend, name):
#             permissions.update(getattr(backend, name)(self, obj))
#     return permissions


class CustomPermissionMixin(models.Model):
    """
    This mixin is used to add the fields of permissions and groups to the user model
    """
    permissions_per_url = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions per url"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    # def get_user_permissions_per_url(self, obj=None):
    #     return _user_get_permissions_per_url(self, obj, 'user')

    # def get_all_permissions_per_url(user, obj=None):
    #     return _user_get_permissions_per_url(user, obj, 'all')

    # def has_perm_per_url(self, perm, obj=None):
    #     """
    #     Returns True if the user has the specified permission for the url.
    #     """
    #     # Active superusers have all permissions.
    #     if self.is_active and self.is_superuser:
    #         return True
    #
    #     # Otherwise we need to check the backends.
    #     return _user_has_perm_per_url(self, perm, obj)

    # def has_perms_per_url(self, perm_list, obj=None):
    #     """
    #     Returns True if the user has each of the specified permissions for the url.
    #     """
    #     if not is_iterable(perm_list) or isinstance(perm_list, str):
    #         raise ValueError("perm_list must be an iterable of permissions.")
    #     return all(self.has_perm_per_url(perm, obj) for perm in perm_list)


class User(AbstractUser, CustomPermissionMixin):
    objects = CustomUserManager()
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email']

    class Meta:
        indexes = [
            models.Index(fields=['email', ]),
        ]
