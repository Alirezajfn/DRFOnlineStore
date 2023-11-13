from django.db import models


class Permission(models.Model):
    url = models.CharField(max_length=255)
    codename = models.CharField(max_length=255, null=True, blank=True)
    view = models.CharField(max_length=255)

    def __str__(self):
        return self.codename + ' ' + self.url
