from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def __create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()

        if not email:
            raise ValueError("email was not provided")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self.__create_user(email, password, True, False, **extra_fields)

    def create_superuser(self, email, password=None, is_seller=False, **extra_fields):
        return self.__create_user(
            email, password, True, True, is_seller=is_seller, **extra_fields
        )
