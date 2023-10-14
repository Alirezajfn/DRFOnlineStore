from django.db import models
from django.utils.text import slugify

from users.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveBigIntegerField(default=0)
    main_image = models.ImageField(upload_to='products/')
    stock_quantity = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='products')
    categories = models.ManyToManyField('category.Category', related_name='products', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            suffix = 0
            while Product.objects.filter(slug=self.slug).exists():
                suffix += 1
                self.slug = slugify(self.name) + '-' + str(suffix)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return str(self.product)
