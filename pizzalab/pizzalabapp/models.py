from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Ingredient(models.Model):
    """
    Model class representing an Ingredient object
    """
    name = models.CharField(max_length=50, unique=True)
    is_allergen = models.BooleanField(default=False)
    has_lactose = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class Pizza(models.Model):
    """
    Model class representing a Pizza object
    """
    name = models.CharField(max_length=50, unique=True)
    price = models.PositiveIntegerField()
    ingredients = models.ManyToManyField(
        Ingredient, related_name="pizzas"
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    """
    Model class representing an Order object
    """

    class Meta:
        ordering = ['-id']

    class Status(models.TextChoices):
        AWAITING_PAYMENT = 'AP', _('Awaiting Payment')
        PAYMENT_RECEIVED = 'PR', _('Payment Received')
        PAYMENT_UPDATED = 'PU', _('Payment Updated')
        COMPLETED = 'CO', _('Completed')
        REFUNDED_PARTIALLY = 'RP', _('Refunded Partially')
        REFUNDED = 'RE', _('Refunded')
        CANCELLED = 'CA', _('Cancelled')
        FAILED = 'FA', _('Failed')
        EXPIRED = 'EX', _('Expired')

    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', _('CASH')
        CARD = 'CARD', _('CARD')

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.AWAITING_PAYMENT,
    )
    payment_method = models.CharField(
        max_length=4,
        choices=PaymentMethod.choices,
        default=''
    )
    delivery_address = models.CharField(max_length=150)
    total_price = models.PositiveIntegerField(default=0, null=True)
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'''Order id:{self.id},
        Customer: {self.customer},
        Total Price: {self.total_price}'''

    def get_total_price(self):
        total_price = 0
        for item in self.order_items.all():
            total_price += item.pizza.price * item.quantity

        return total_price


class OrderItem(models.Model):
    """
    Model class representing an OrderItem object
    """
    quantity = models.PositiveIntegerField(default=1)
    pizza = models.ForeignKey(Pizza,
                              related_name="order_items",
                              on_delete=models.CASCADE)
    order = models.ForeignKey(Order,
                              related_name='order_items',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pizza} x {self.quantity}'
