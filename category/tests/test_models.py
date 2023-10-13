from django.test import TestCase
from model_bakery import baker

from category.models import Category


class UserManagerTests(TestCase):

    def test_create_category(self):
        category = Category.objects.create(
            name="category"
        )
        self.assertEquals(category.name, "category")
        self.assertEquals(category.slug, "category")

    def test_create_category_with_duplicate_name(self):
        Category.objects.create(
            name="category"
        )

        category = Category.objects.create(
            name="category"
        )
        self.assertEquals(category.name, "category")
        self.assertEquals(category.slug, "category-1")
