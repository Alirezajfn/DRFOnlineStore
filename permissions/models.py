from django.db import models


class PermissionPerUrls(models.Model):
    url = models.CharField(max_length=255)
    codename = models.CharField(max_length=255, unique=True, db_index=True)
    view = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.codename
