from accounts.models import Account
from django.db.utils import IntegrityError
from django.test import TestCase


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.email = "alex@mail.com"
        cls.password = "abcd"
        cls.first_name = "christian"
        cls.last_name = "bezerra"
        cls.is_seller = True

        cls.account = Account.objects.create_user(
            email=cls.email,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
            is_seller=cls.is_seller,
        )

    def test_create_duplicate_account(self):
        with self.assertRaises(IntegrityError):
            Account.objects.create_user(
                email=self.email,
                password=self.password,
                first_name=self.first_name,
                last_name=self.last_name,
                is_seller=self.is_seller,
            )

    def test_user_has_equal_information_fields(self):
        self.assertIsNotNone(self.account.id)
        self.assertIsNotNone(self.account.password)
        self.assertEqual(self.account.email, self.email)
        self.assertEqual(self.account.first_name, self.first_name)
        self.assertEqual(self.account.last_name, self.last_name)
        self.assertEqual(self.account.is_seller, self.is_seller)
