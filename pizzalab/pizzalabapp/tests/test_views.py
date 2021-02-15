import io

from django.contrib.auth import get_user_model
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from pizzalabapp.models import Pizza, OrderItem


class PizzaListViewSet(APITestCase):
    fixtures = ['ingredients.json', 'pizzas.json']

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
    fixtures = ['ingredients.json', 'pizzas.json']

    def setUp(self):
        self.pizza = Pizza.objects.first()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/pizzas/{self.pizza.id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse('pizza-detail', args=[self.pizza.id])
        )
        self.assertEqual(response.status_code, 200)


class OrderListViewSet(APITestCase):
    fixtures = ['ingredients.json', 'pizzas.json', 'users.json',
                'orders.json', 'order_items.json']

    def setUp(self):
        self.staff_user = get_user_model().objects.get(username='pav')
        self.just_user = get_user_model().objects.get(username='ion')

    def test_get_queryset_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('order-list'))
        stream = io.BytesIO(response.content)
        content = JSONParser().parse(stream)
        self.assertEqual(content.get('count'), 17)

    def test_get_queryset_non_staff(self):
        self.client.force_login(self.just_user)
        response = self.client.get(reverse('order-list'))
        stream = io.BytesIO(response.content)
        content = JSONParser().parse(stream)
        self.assertEqual(content.get('count'), 1)

    def test_post_staff_customer_requested(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(
            reverse('order-list'),
            data={
                "order_items": [
                    {
                        "pizza": {
                            "name": "Dubiosa"
                        },
                        "quantity": 1
                    }
                ],
                "payment_method": "CASH",
                "delivery_address": "Home",
                "customer": self.just_user.id
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_post_staff_customer_not_requested(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(
            reverse('order-list'),
            data={
                "order_items": [
                    {
                        "pizza": {
                            "name": "Dubiosa"
                        },
                        "quantity": 1
                    }
                ],
                "payment_method": "CASH",
                "delivery_address": "Home",
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_post_non_staff_customer_requested(self):
        self.client.force_login(self.just_user)
        response = self.client.post(
            reverse('order-list'),
            data={
                "order_items": [
                    {
                        "pizza": {
                            "name": "Dubiosa"
                        },
                        "quantity": 1
                    }
                ],
                "payment_method": "CASH",
                "delivery_address": "Home",
                "customer": self.staff_user.id
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_post_non_staff_customer_not_requested(self):
        self.client.force_login(self.just_user)
        response = self.client.post(
            reverse('order-list'),
            data={
                "order_items": [
                    {
                        "pizza": {
                            "name": "Dubiosa"
                        },
                        "quantity": 1
                    }
                ],
                "payment_method": "CASH",
                "delivery_address": "Home",
            }
        )
        self.assertEqual(response.status_code, 201)


class UserListViewSet(APITestCase):

    def test_create_user(self):
        response = self.client.post(
            reverse('user-list'),
            data={
                "username": "autotestuser",
                "email": "autotest@example.com",
                "password": "autotestpassword"
            }
        )
        self.assertEqual(response, 201)
