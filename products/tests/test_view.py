from accounts.models import Account
from products.models import Product
from products.serializers import ProductCreateSerializer, ProductListSerializer
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class ProductViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.product = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
        }
        cls.productError1 = {
            "price": 100.99,
            "quantity": 15,
        }
        cls.productError2 = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": -15,
        }
        cls.seller = Account.objects.create_user(
            email="cb@mail.com",
            password="1234",
            first_name="christian",
            last_name="bezerra",
            is_seller=True,
        )
        cls.commum = Account.objects.create_user(
            email="cbm@mail.com",
            password="1234",
            first_name="christian",
            last_name="bezerra",
            is_seller=False,
        )
        cls.tokenSeller = Token.objects.create(user=cls.seller)
        cls.tokenCommum = Token.objects.create(user=cls.commum)

    def test_only_seller_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenSeller.key)
        response = self.client.post("/api/products/", self.product)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["seller"]["id"], self.seller.id)

    def test_only_seller_create_product_with_no_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenCommum.key)
        response = self.client.post("/api/products/", self.product)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_only_owner_product_can_update_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenSeller.key)
        self.client.post("/api/products/", self.product)
        response = self.client.patch(f"/api/products/1/", {"description": "Teste name"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], "Teste name")

    def test_only_owner_product_can_update_product_with_no_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenSeller.key)
        self.client.post("/api/products/", self.product)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenCommum.key)
        response = self.client.patch(f"/api/products/1/", {"description": "Teste name"})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_any_list_products(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenSeller.key)
        for _ in range(10):
            self.client.post("/api/products/", self.product)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenCommum.key)
        response = self.client.get("/api/products/")

        self.assertEqual(len(response.data), 10)

    def test_any_filter_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenSeller.key)
        self.client.post("/api/products/", self.product)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenCommum.key)
        response = self.client.get("/api/products/1/")

        self.assertIsNotNone(response.data["seller_id"])

    def test_list_return(self):
        product = Product.objects.create(**self.product, seller=self.seller)
        response = self.client.get(f"/api/products/{product.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductListSerializer(instance=product).data, response.data)

    def test_create_return(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenSeller.key)
        response = self.client.post(f"/api/products/", self.product)
        serializer = ProductCreateSerializer(data=response.data)

        serializer.is_valid(raise_exception=True)
        self.assertEqual(response.status_code, 201)

    def test_keys_errors(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenSeller.key)
        response = self.client.post(f"/api/products/", self.productError1)

        self.assertEqual(response.data["description"][0], "This field is required.")

    def test_negative_quantity(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenSeller.key)
        response = self.client.post(f"/api/products/", self.productError2)

        self.assertEqual(response.data["quantity"][0], "quantity cannot be negative")
