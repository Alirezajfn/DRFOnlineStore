from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from product.models import Product
from category.models import Category


class ProductTests(APITestCase):

    def setUp(self) -> None:
        self.user = baker.make(get_user_model(), is_staff=True, is_superuser=True)
        self.categories = baker.make(Category, _quantity=3)
        self.client.force_login(self.user)

        image = BytesIO()
        Image.new('RGB', (100, 100)).save(image, 'JPEG')
        image.seek(0)
        self.main_image = SimpleUploadedFile('image.jpg', image.getvalue())

    def test_create_product_successfully(self):
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': [self.categories[0].slug],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
            'main_image': self.main_image,
        }
        response = self.client.post(reverse('product:product-list'), data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Product.objects.count(), 1)

    def test_create_product_without_being_authenticated(self):
        self.client.logout()
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': [self.categories[0].slug],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
            'main_image': self.main_image,
        }
        response = self.client.post(reverse('product:product-list'), data)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(Product.objects.count(), 0)

    def test_create_product_without_being_staff(self):
        self.user.is_staff = False
        self.user.save()
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': [self.categories[0].slug],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
            'main_image': self.main_image,
        }
        response = self.client.post(reverse('product:product-list'), data)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(Product.objects.count(), 0)

    def test_create_product_with_invalid_category(self):
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': ['invalid-category'],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
            'main_image': self.main_image,
        }
        response = self.client.post(reverse('product:product-list'), data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Product.objects.count(), 0)

    def test_create_product_with_image(self):
        image = BytesIO()
        Image.new('RGB', (100, 100)).save(image, 'JPEG')
        image.seek(0)
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': [self.categories[0].slug],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
            'main_image': self.main_image,
            'images': [SimpleUploadedFile('image.jpg', image.getvalue())],
        }
        response = self.client.post(reverse('product:product-list'), data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Product.objects.count(), 1)
        self.assertEquals(Product.objects.first().images.count(), 1)

    def test_create_product_with_invalid_category_and_valid_category(self):
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': ['invalid-category', self.categories[0].slug],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
            'main_image': self.main_image,
        }
        response = self.client.post(reverse('product:product-list'), data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Product.objects.count(), 0)

    def test_update_product_successfully(self):
        product = baker.make(Product)
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': [self.categories[0].slug],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
            'main_image': self.main_image,
        }
        response = self.client.put(reverse('product:product-detail', args=[product.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Product.objects.count(), 1)
        self.assertEquals(Product.objects.first().name, 'Product')

    def test_update_product_with_categories(self):
        product = baker.make(Product)
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': [self.categories[0].slug, self.categories[1].slug],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
            'main_image': self.main_image,
        }
        response = self.client.put(reverse('product:product-detail', args=[product.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Product.objects.count(), 1)
        self.assertEquals(Product.objects.first().categories.count(), 2)

    def test_update_with_invalid_category(self):
        product = baker.make(Product)
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': ['invalid-category'],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
            'main_image': self.main_image,
        }
        response = self.client.put(reverse('product:product-detail', args=[product.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Product.objects.count(), 1)
        self.assertEquals(Product.objects.first().categories.count(), 0)

    def test_update_with_image(self):
        product = baker.make(Product)
        image = BytesIO()
        Image.new('RGB', (100, 100)).save(image, 'JPEG')
        image.seek(0)
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': [self.categories[0].slug],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
            'main_image': self.main_image,
            'images': [SimpleUploadedFile('image.jpg', image.getvalue())],
        }
        response = self.client.put(reverse('product:product-detail', args=[product.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Product.objects.count(), 1)
        self.assertEquals(Product.objects.first().images.count(), 1)

    def test_update_product_without_being_authenticated(self):
        self.client.logout()
        product = baker.make(Product)
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': [self.categories[0].slug],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
        }
        response = self.client.put(reverse('product:product-detail', args=[product.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(Product.objects.count(), 1)
        self.assertEquals(Product.objects.first().name, product.name)

    def test_update_product_without_being_admin(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        product = baker.make(Product)
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': [self.categories[0].slug],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
        }
        response = self.client.patch(reverse('product:product-detail', args=[product.slug]), data)
        print(response.data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(Product.objects.count(), 1)
        self.assertEquals(Product.objects.first().name, product.name)

    def test_update_product_without_being_owner(self):
        product = baker.make(Product)
        self.client.logout()
        self.client.force_login(baker.make(get_user_model()))
        data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': [self.categories[0].slug],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
        }
        response = self.client.patch(reverse('product:product-detail', args=[product.slug]), data)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(Product.objects.count(), 1)
        self.assertEquals(Product.objects.first().name, product.name)

    def test_list_products(self):
        baker.make(Product, _quantity=3)
        response = self.client.get(reverse('product:product-list'))

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], 3)

    def test_return_only_active_products(self):
        baker.make(Product, _quantity=3)
        baker.make(Product, _quantity=2, is_active=False)
        response = self.client.get(reverse('product:product-list'))

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], 3)

    def test_retrieve_product(self):
        product = baker.make(Product)
        response = self.client.get(reverse('product:product-detail', args=[product.slug]))

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['name'], product.name)

    def test_retrieve_inactive_product(self):
        product = baker.make(Product, is_active=False)
        response = self.client.get(reverse('product:product-detail', args=[product.slug]))

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_product_with_invalid_slug(self):
        response = self.client.get(reverse('product:product-detail', args=['invalid-slug']))

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product(self):
        product = baker.make(Product)
        response = self.client.delete(reverse('product:product-detail', args=[product.slug]))

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Product.objects.count(), 0)

    def test_delete_product_without_being_authenticated(self):
        self.client.logout()
        product = baker.make(Product)
        response = self.client.delete(reverse('product:product-detail', args=[product.slug]))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(Product.objects.count(), 1)

    def test_delete_product_without_being_superuser(self):
        self.user.is_superuser = False
        self.user.is_staff = True
        self.user.save()
        product = baker.make(Product)
        response = self.client.delete(reverse('product:product-detail', args=[product.slug]))

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(Product.objects.count(), 1)

    def test_delete_product_by_creator(self):
        self.user.is_superuser = False
        self.user.is_staff = True
        self.user.save()
        product = baker.make(Product, creator=self.user)

        self.client.force_login(self.user)
        response = self.client.delete(reverse('product:product-detail', args=[product.slug]))

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Product.objects.count(), 0)

    def test_delete_product_with_sales_count_greater_than_zero(self):
        product = baker.make(Product, sales_count=1)
        response = self.client.delete(reverse('product:product-detail', args=[product.slug]))

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Product.objects.count(), 1)
