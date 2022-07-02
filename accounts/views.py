from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView, Response, status

from .models import Account
from .permissions import IsAdmin, IsOwner
from .serializers import (
    AccountLoginSerializer,
    AccountSerializer,
    AccountUpdateSerializer,
)


class ListCreateView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ListNewestView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        max = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:max]


class UpdateAccountView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class UpdateActiveAccountView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    queryset = Account.objects.all()
    serializer_class = AccountUpdateSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = AccountLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "invalid email or password"}, status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})
