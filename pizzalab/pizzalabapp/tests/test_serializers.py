from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from pizzalabapp.models import Order, OrderItem, Pizza
from pizzalabapp.serializers import (OrderItemListSerializer,
                                     OrderItemSerializer, OrderSerializer,
                                     PizzaSerializer)
from userapp.serializers import UserSerializer


class PizzaTestCase(APITestCase):
    fixtures = ['ingredients.json', 'pizzas.json']

    def setUp(self):
        self.pizza = Pizza.objects.get(name="Pizza 0")
        self.pizza_safe_ingr = Pizza.objects.get(name="Pizza 10")
        self.pizza_unsafe_ingr = Pizza.objects.get(name="Dubiosa")

        # HyperlinkedIdentityField requiring Request workaround:
        factory = APIRequestFactory()
        request = factory.get('/')
        self.serializer_context = {
            'request': Request(request),
        }

        self.pizza_serializer = PizzaSerializer(
            instance=self.pizza,
            context=self.serializer_context
        )

    def test_create_pizza(self):
        new_pizza_data = {
            "ingredients": [{
                "name": "Șuncă"
            }, {
                "name": "Ceapă"
            }],
            "name": "NewPizza",
            "price": 9
        }
        new_pizza_ser = PizzaSerializer(
            data=new_pizza_data,
            context=self.serializer_context
        )
        self.assertEqual(new_pizza_ser.is_valid(), True)
        new_pizza_ser.save()
        self.assertEqual(new_pizza_ser.data.get('price'), 9)

    def test_inexistent_ingredients_invalid(self):
        self.pizza_serializer.data['ingredients'] += [{"name": "NewIngrr"}]
        new_pizza_data = self.pizza_serializer.data
        new_pizza_serializer = PizzaSerializer(data=new_pizza_data)
        self.assertFalse(new_pizza_serializer.is_valid())
        self.assertIsNotNone(new_pizza_serializer.errors.get('ingredients'))

    def test_edit_price(self):
        # get existing pizza data
        data = self.pizza_serializer.data
        data['price'] = 13

        # edit the existing pizza with the updated price
        self.client.put(
            reverse('pizza-detail', args=[self.pizza.id]),
            data
        )

        # verify that the price has been updated
        self.pizza.refresh_from_db()
        self.assertEqual(self.pizza.price, 13)

    def test_has_allergens(self):
        serializer = PizzaSerializer(
            self.pizza_unsafe_ingr,
            context=self.serializer_context
        )
        self.assertEqual(
            serializer.data.get('has_allergen_ingredients'), True
        )

    def test_has_lactose(self):
        serializer = PizzaSerializer(
            self.pizza_safe_ingr,
            context=self.serializer_context
        )
        self.assertEqual(
            serializer.data.get('has_lactose_ingredients'), False
        )


class OrderItemTestCase(APITestCase):
    fixtures = ['ingredients.json', 'pizzas.json', 'users.json',
                'orders.json', 'order_items.json']

    def setUp(self):
        self.order_item = OrderItem.objects.first()
        self.order_item_serializer = OrderItemSerializer(self.order_item)

    def test_inexistent_pizza_invalid(self):
        data = self.order_item_serializer.data
        data['pizza'] = {"name": "IDoNotExist"}
        data['quantity'] = 1
        new_serializer = OrderItemListSerializer(data=data)
        self.assertFalse(new_serializer.is_valid())
        self.assertIsNotNone(new_serializer.errors.get('pizza'))

    def test_existing_pizza_valid(self):
        data = self.order_item_serializer.data
        data['pizza'] = {"name": "Margherita"}
        data['quantity'] = 2
        new_order_item = OrderItemListSerializer(data=data)
        self.assertEqual(new_order_item.is_valid(), True)


class OrderTestCase(APITestCase):
    fixtures = ['ingredients.json', 'pizzas.json', 'users.json',
                'orders.json', 'order_items.json']

    def setUp(self):
        self.order = Order.objects.first()
        self.order_serializer = OrderSerializer(self.order)
        self.user = get_user_model().objects.get(username="pav")

    def test_create_order(self):
        new_order_item = {
            "pizza": {
                "name": "Margherita",
            },
            "quantity": 1,
            "order_id": self.order.id
        }
        new_order = {
            'order_items': [new_order_item],
            'customer': f"{self.user.id}",
            'delivery_address': "HOME",
            'payment_method': "CASH"
        }
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('order-list'),
            data=new_order
        )
        self.assertEqual(response.status_code, 201)
