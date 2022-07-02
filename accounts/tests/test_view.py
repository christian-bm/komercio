from accounts.models import Account
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class AccountViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.sellerData = {
            "email": "cb@mail.com",
            "password": "1234",
            "first_name": "christian",
            "last_name": "bezerra",
            "is_seller": True,
        }
        cls.sellerDataIncorrect = {
            "email": "cb",
            "password": "1234",
            "first_name": "christian",
            "last_name": "bezerra",
            "is_seller": True,
        }

        cls.commumData = {
            "email": "cb@mail.com",
            "password": "1234",
            "first_name": "christian",
            "last_name": "bezerra",
            "is_seller": False,
        }
        cls.commumDataIncorrect = {
            "email": "cb",
            "password": "1234",
            "first_name": "christian",
            "last_name": "bezerra",
            "is_seller": False,
        }

    def test_create_seller_account(self):
        response = self.client.post("/api/accounts/", self.sellerData, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["is_seller"], True)

    def test_create_seller_account_with_incorrect_key(self):
        response = self.client.post(
            "/api/accounts/", self.sellerDataIncorrect, format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0], "Enter a valid email address.")

    def test_create_commum_account(self):
        response = self.client.post("/api/accounts/", self.commumData, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["is_seller"], False)

    def test_create_commum_account_with_incorrect_key(self):
        response = self.client.post(
            "/api/accounts/", self.commumDataIncorrect, format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0], "Enter a valid email address.")

    def test_login_seller_return_token(self):
        self.client.post("/api/accounts/", self.sellerData, format="json")
        response = self.client.post(
            "/api/login/",
            {
                "email": self.sellerData["email"],
                "password": self.sellerData["password"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "token")

    def test_login_commum_return_token(self):
        self.client.post("/api/accounts/", self.commumData, format="json")
        response = self.client.post(
            "/api/login/",
            {
                "email": self.commumData["email"],
                "password": self.commumData["password"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "token")


class TestPermisionsView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
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
        cls.admin = Account.objects.create_superuser(
            email="cbm123@mail.com",
            password="1234",
            first_name="christian",
            last_name="bezerra",
            is_seller=False,
        )
        cls.tokenSeller = Token.objects.create(user=cls.seller)
        cls.tokenCommum = Token.objects.create(user=cls.commum)
        cls.tokenAdmin = Token.objects.create(user=cls.admin)

    def test_only_owner_update_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenSeller.key)
        response = self.client.patch(
            f"/api/accounts/{self.seller.id}/", {"first_name": "Nome teste"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "Nome teste")

    def test_only_owner_update_data_with_no_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenCommum.key)
        response = self.client.patch(
            f"/api/accounts/{self.seller.id}/", {"first_name": "Novo nome"}
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_only_admin_update_status_account(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenAdmin.key)
        response = self.client.patch(
            f"/api/accounts/{self.seller.id}/management/", {"is_active": False}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["is_active"], False)

    def test_only_admin_update_status_account_with_no_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenSeller.key)
        response = self.client.patch(
            f"/api/accounts/{self.seller.id}/management/", {"is_active": True}
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_any_list_all_accounts(self):
        response = self.client.get("/api/accounts/")

        self.assertEqual(len(response.data), 3)
