from django.test import TestCase

from pizzalabapp.models import Ingredient, OrderItem, Pizza

from .helpers import setup_return_order


class IngredientTestCase(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='AutoIngredient')

    def test_name_label(self):
        field_label = self.ingredient._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_str(self):
        self.assertEqual(str(self.ingredient), 'AutoIngredient')


class PizzaTestCase(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='AutoIngredient')
        self.pizza = Pizza.objects.create(name="AutoPizza", price=420)
        self.pizza.ingredients.add(self.ingredient)

    def test_name_label(self):
        field_label = self.pizza._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_str(self):
        self.assertEqual(str(self.pizza), 'AutoPizza')


class OrderItemTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_return_order()

    def test_str(self):
        order_item = OrderItem.objects.get(id=1)
        self.assertEqual(str(order_item), "AutoPizza x 5")


class OrderTestCase(TestCase):

    def setUp(self):
        self.order = setup_return_order()

    def test_str(self):
        self.assertEqual(
            str(self.order), "Order id: 3,\
                Customer: testuser,\
                Total Price: 50"
        )

    def test_calculate_total_price(self):
        self.assertEqual(
            self.order.total_price, 50
        )
