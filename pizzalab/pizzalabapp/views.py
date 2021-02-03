from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from pizzalabapp.models import Ingredient, Order, OrderItem, Pizza
from pizzalabapp.serializers import (IngredientSerializer, OrderItemSerializer,
                                     OrderSerializer, PizzaSerializer)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer_requested = self.request.data.get('customer')
        user = self.request.user
        if customer_requested and user.is_staff:
            serializer.save(
                customer=get_user_model().objects.get(
                    id=customer_requested
                )
            )
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        elif customer_requested and not user.is_staff:
            return Response(
                "Ordering for other customers is prohibited",
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer.save(customer=user)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return Order.objects.filter(customer=user)
        else:
            return Order.objects.all()


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
