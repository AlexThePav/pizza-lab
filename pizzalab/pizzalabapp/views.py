from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

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
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        customer_requested = self.request.data.get('customer')
        if self.request.user.is_staff and customer_requested:
            serializer.save(
                customer=get_user_model().objects.get(
                    id=customer_requested
                )
            )
        else:
            serializer.save(customer=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
