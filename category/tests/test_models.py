from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker

from category.models import Category


class CategoryTests(TestCase):

    def test_create_category(self):
        category = Category.objects.create(
            name="category",
            creator=baker.make(get_user_model(), is_staff=True, is_superuser=True)
        )
        self.assertEquals(category.name, "category")
        self.assertEquals(category.slug, "category")

    def test_create_category_with_duplicate_name(self):
        Category.objects.create(
            name="category",
            creator=baker.make(get_user_model(), is_staff=True, is_superuser=True)
        )

        category = Category.objects.create(
            name="category",
            creator=baker.make(get_user_model(), is_staff=True, is_superuser=True)
        )
        self.assertEquals(category.name, "category")
        self.assertEquals(category.slug, "category-1")
