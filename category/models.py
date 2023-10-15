from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=3000, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children', blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255)
    creator = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT, related_name='categories')
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            suffix = 0
            while Category.objects.filter(slug=self.slug).exists():
                suffix += 1
                self.slug = slugify(self.name) + '-' + str(suffix)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        if self.parent is None:
            return self.name
        return f"{self.parent}/{self.name}"
