from accounts.models import Account
from django.db.utils import IntegrityError
from django.test import TestCase
from products.models import Product


class ProductModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.description = "Smartband XYZ 3.0"
        cls.price = 100.99
        cls.quantity = 15

        cls.seller = Account.objects.create_user(
            email="alex@mail.com",
            password="abcd",
            first_name="christian",
            last_name="bezerra",
            is_seller=True,
        )
        cls.product = Product(
            description=cls.description, price=cls.price, quantity=cls.quantity
        )

    def test_create_product_without_seller(self):
        with self.assertRaises(IntegrityError):
            self.product.save()

    def test_create_product_with_seller(self):
        self.product.seller = self.seller
        self.product.save()

    def test_product_fields(self):
        self.product.seller = self.seller
        self.product.save()

        self.assertEqual(self.product.seller, self.seller)
        self.assertEqual(self.product.description, self.description)
        self.assertEqual(self.product.price, self.price)
        self.assertEqual(self.product.quantity, self.quantity)
