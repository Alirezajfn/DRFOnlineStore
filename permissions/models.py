from django.db import models


class UrlsGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PermissionPerUrls(models.Model):
    url = models.CharField(max_length=255)
    codename = models.CharField(max_length=255, unique=True, db_index=True)
    view = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    app_name = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(UrlsGroup, on_delete=models.CASCADE, related_name='permissions', null=True, blank=True)

    def __str__(self):
        return self.codename


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    permissions = models.ManyToManyField(PermissionPerUrls, related_name='roles', blank=True)

    def __str__(self):
        return self.name
