from accounts.serializers import AccountSerializer
from rest_framework import serializers

from .models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    seller = AccountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "seller", "description", "price", "quantity", "is_active"]
        read_only_fields = ["id", "seller", "is_active"]
        depth = 1

    def create(self, validated_data: dict):
        return Product.objects.create(**validated_data)

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("quantity cannot be negative")

        return value


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["description", "price", "quantity", "is_active", "seller_id"]
