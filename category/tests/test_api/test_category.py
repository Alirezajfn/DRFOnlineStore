from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from category.models import Category


class CategoryTests(APITestCase):

    def setUp(self) -> None:
        self.user = baker.make(get_user_model(), is_staff=True, is_superuser=True)
        self.client.force_login(self.user)

    def test_create_category_without_parent_successfully(self):
        data = {
            'name': 'Category'
        }
        response = self.client.post(reverse('category:category-list'), data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Category.objects.count(), 1)

    def test_create_category_with_parent_successfully(self):
        parent = baker.make(Category)
        data = {
            'name': 'Category',
            'parent': parent.slug
        }
        response = self.client.post(reverse('category:category-list'), data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Category.objects.count(), 2)

    def test_create_category_with_invalid_parent(self):
        data = {
            'name': 'Category',
            'parent': 'invalid'
        }
        response = self.client.post(reverse('category:category-list'), data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Category.objects.count(), 0)

    def test_create_category_without_being_authenticated(self):
        self.client.logout()

        data = {
            'name': 'Category'
        }
        response = self.client.post(reverse('category:category-list'), data)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(Category.objects.count(), 0)

    def test_create_category_without_being_admin_or_staff(self):
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()

        data = {
            'name': 'Category'
        }
        response = self.client.post(reverse('category:category-list'), data)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(Category.objects.count(), 0)

    def test_update_category_without_parent_successfully(self):
        category = baker.make(Category)
        data = {
            'name': 'Category'
        }
        response = self.client.put(reverse('category:category-detail', args=[category.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Category.objects.count(), 1)

    def test_update_category_with_parent_successfully(self):
        parent = baker.make(Category)
        category = baker.make(Category)
        data = {
            'name': 'Category',
            'parent': parent.slug
        }
        response = self.client.put(reverse('category:category-detail', args=[category.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Category.objects.count(), 2)

    def test_update_category_with_invalid_parent(self):
        category = baker.make(Category)
        data = {
            'name': 'Category',
            'parent': 'invalid'
        }
        response = self.client.put(reverse('category:category-detail', args=[category.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Category.objects.count(), 1)

    def test_update_category_without_being_authenticated(self):
        self.client.logout()

        category = baker.make(Category)
        data = {
            'name': 'Category'
        }
        response = self.client.put(reverse('category:category-detail', args=[category.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(Category.objects.count(), 1)

    def test_update_category_without_being_admin_or_staff(self):
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()

        category = baker.make(Category)
        data = {
            'name': 'Category'
        }
        response = self.client.put(reverse('category:category-detail', args=[category.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(Category.objects.count(), 1)

    def test_update_category_with_self_parent(self):
        category = baker.make(Category)
        data = {
            'name': 'Category',
            'parent': category.slug
        }
        response = self.client.put(reverse('category:category-detail', args=[category.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Category.objects.count(), 1)

    def test_update_category_with_parent_that_is_child_of_itself(self):
        parent = baker.make(Category)
        category = baker.make(Category, parent=parent)
        data = {
            'name': 'Category',
            'parent': category.slug
        }
        response = self.client.put(reverse('category:category-detail', args=[parent.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Category.objects.count(), 2)

    def test_retrieve_category_with_parent_and_children_successfully(self):
        parent = baker.make(Category)
        category = baker.make(Category, parent=parent)
        baker.make(Category, parent=category, _quantity=5)
        baker.make(Category, _quantity=5)

        response = self.client.get(reverse('category:category-detail', args=[category.slug]))

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['children']), 5)
        self.assertEquals(Category.objects.filter(parent__slug=category.slug).count(), 5)
