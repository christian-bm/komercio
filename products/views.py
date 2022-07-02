from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from .mixins import SerializerByMethodMixin
from .models import Product
from .permissions import IsOwnerOrReadOnly, IsSellerOrReadOnly
from .serializers import ProductCreateSerializer, ProductListSerializer


class ListCreateProductView(SerializerByMethodMixin, ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]

    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductListSerializer,
        "POST": ProductCreateSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class RetrieveUpdateProductView(SerializerByMethodMixin, RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductListSerializer,
        "PATCH": ProductCreateSerializer,
    }
