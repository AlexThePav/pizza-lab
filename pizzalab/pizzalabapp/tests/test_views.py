from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from pizzalabapp.models import Pizza

from .helpers import setup_pizzas


class PizzaListViewSet(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        setup_pizzas(15)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/pizzas/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('pizza-list'))
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('pizza-list'))
        self.assertEqual(response.status_code, 200)


class PizzaDetailViewSet(APITestCase):

    @classmethod
    def setUpTestData(cls):
        setup_pizzas(1)

    def setUp(self):
        self.pizza = Pizza.objects.get(name="Pizza 0")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/pizzas/{self.pizza.id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse('pizza-detail', args=[self.pizza.id])
        )
        self.assertEqual(response.status_code, 200)
