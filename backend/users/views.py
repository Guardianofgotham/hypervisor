from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from users.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

from rest_framework.decorators import action
from rest_framework.authtoken.models import Token


# Create your views here.
class UserViewSet(ViewSet):
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                data=UserSerializer(user).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=False)
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={"token": token.key, "username": user.username})

        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )
