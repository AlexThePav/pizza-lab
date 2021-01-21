from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_allergen = models.BooleanField(default=False)
    has_lactose = models.BooleanField(default=False)


class Pizza(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.PositiveIntegerField()
    ingredient = models.ManyToManyField(Ingredient)


class Order(models.Model):

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
    total_price = models.PositiveIntegerField(default=0)
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
