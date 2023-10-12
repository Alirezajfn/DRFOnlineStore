from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent}/{self.name}"
