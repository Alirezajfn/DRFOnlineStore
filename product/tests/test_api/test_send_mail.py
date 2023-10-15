from io import BytesIO
from unittest.mock import patch

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from model_bakery import baker


from product.models import Product
from category.models import Category


class SendMailTests(TestCase):

    def setUp(self) -> None:
        self.active_superusers = baker.make(get_user_model(), is_superuser=True, is_active=True, _quantity=2)
        self.user = baker.make(get_user_model(), is_superuser=False, is_staff=True, is_active=True)

        self.client.force_login(self.user)
        self.url = reverse('product:product-list')


        image = BytesIO()
        Image.new('RGB', (100, 100)).save(image, 'JPEG')
        image.seek(0)

        self.categories = baker.make(Category, _quantity=2)
        self.main_image = SimpleUploadedFile('image.jpg', image.getvalue())
        self.data = {
            'name': 'Product',
            'description': 'Product description',
            'categories': [self.categories[0].slug],
            'price': 1000,
            'quantity': 10,
            'stock_quantity': 10,
            'main_image': self.main_image,
        }

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    @patch('product.services.celery.MailSenderManager.send')
    def test_send_mail_when_create_product(self, send_mock):
        send_mock.return_value = 2

        response = self.client.post(self.url, data=self.data)

        self.assertTrue(response.status_code, 201)
        self.assertTrue(send_mock.called)
        self.assertEquals(send_mock.call_count, 1)

        send_mock.assert_called_once_with(
            to_email=[admin.email for admin in self.active_superusers],
            message=f'New product added: {Product.objects.last().name}',
            title=f'New product added: {Product.objects.last().name}'
        )
