from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from userapp.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        try:
            get_user_model().objects.create_user(
                username=request.data['username'],
                password=request.data['password'],
                email=request.data['email'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name']
            )
            return Response(
                "User created!", status=status.HTTP_201_CREATED
            )
        except IntegrityError as e:
            return Response(
                e.args,
                status.HTTP_409_CONFLICT
            )
