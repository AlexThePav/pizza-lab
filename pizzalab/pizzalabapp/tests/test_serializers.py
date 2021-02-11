import io

from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from pizzalabapp.models import OrderItem, Pizza
from pizzalabapp.serializers import OrderItemSerializer, PizzaSerializer

from .helpers import setup_pizzas, setup_return_order


class PizzaTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        setup_pizzas(1, True, False)

    def setUp(self):
        self.pizza = Pizza.objects.get(name="Pizza 0")

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

    def test_inexistent_ingredients_invalid(self):
        self.pizza_serializer.data['ingredients'] += [{"name": "NewIngrr"}]
        new_pizza_data = self.pizza_serializer.data
        new_pizza_serializer = PizzaSerializer(data=new_pizza_data)
        self.assertFalse(new_pizza_serializer.is_valid())
        self.assertIsNotNone(new_pizza_serializer.errors.get('ingredients'))

    def test_edit_price(self):
        # get existing pizza details
        current_content = self.client.get(
            reverse('pizza-detail', args=[self.pizza.id])
        ).content

        # setup data with updated price
        stream = io.BytesIO(current_content)
        data = JSONParser().parse(stream)
        data['price'] = 13
        new_data = data

        # edit the existing pizza with the updated price
        response = self.client.put(
            reverse('pizza-detail', args=[self.pizza.id]),
            new_data
        )

        # verify that the price has been updated
        new_content = response.content
        new_stream = io.BytesIO(new_content)
        new_data = JSONParser().parse(new_stream)
        self.assertEqual(new_data.get('price'), 13)

    def test_has_allergens(self):
        self.assertEqual(
            self.pizza_serializer.data.get('has_allergen_ingredients'), True
        )

    def test_has_lactose(self):
        self.assertEqual(
            self.pizza_serializer.data.get('has_lactose_ingredients'), False
        )


class OrderItemTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        setup_return_order()

    def setUp(self):
        self.order_item = OrderItem.objects.first()
        self.order_item_serializer = OrderItemSerializer(self.order_item)

    def test_inexistent_pizza_invalid(self):
        data = self.order_item_serializer.data
        data['pizza'] = 0
        new_serializer = OrderItemSerializer(data=data)
        self.assertFalse(new_serializer.is_valid())
        self.assertIsNotNone(new_serializer.errors.get('pizza'))
