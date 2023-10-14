from django.test import TestCase

from product.models import Product


class ProductTests(TestCase):

    def test_create_product(self):
        product = Product.objects.create(
            name="product",
            price=1000,
            stock_quantity=10,
        )
        self.assertEquals(product.name, "product")
        self.assertEquals(product.slug, "product")

    def test_create_product_with_duplicate_name(self):
        Product.objects.create(
            name="product",
            price=1000,
            stock_quantity=10,
        )

        product = Product.objects.create(
            name="product",
            price=1000,
            stock_quantity=10,
        )
        self.assertEquals(product.name, "product")
        self.assertEquals(product.slug, "product-1")
