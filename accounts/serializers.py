from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_seller",
            "date_joined",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }

    def create(self, validated_data: dict):
        return Account.objects.create_user(**validated_data)


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_seller",
            "date_joined",
            "is_active",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }

    def create(self, validated_data: dict):
        return Account.objects.create_user(**validated_data)


class AccountLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
