from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from product.models import Product
from category.models import Category


class ProductViewSetPaginationTestCase(APITestCase):

    def setUp(self) -> None:
        self.staff_user = baker.make(get_user_model(), is_staff=True)
        self.normal_user = baker.make(get_user_model(), is_staff=False)
        self.category = baker.make(Category)
        self.products = baker.make(Product, _quantity=1500, categories=[self.category])
        self.url = reverse('product:product-list')

    def test_pagination_page_size_as_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url + '?page_size=1000')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), 1000)
        self.assertEquals(response.data['count'], 1500)

    def test_pagination_page_size_as_normal_user(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(self.url + '?page_size=1000')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), 100)
        self.assertEquals(response.data['count'], 1500)

    def test_pagination_page_size_as_anonymous_user(self):
        response = self.client.get(self.url + '?page_size=1000')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), 100)
        self.assertEquals(response.data['count'], 1500)

    def test_pagination_page_size_as_staff_with_default_page_size(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), 10)
        self.assertEquals(response.data['count'], 1500)

    def test_pagination_page_size_as_normal_user_with_default_page_size(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), 10)
        self.assertEquals(response.data['count'], 1500)