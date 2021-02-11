from django.contrib.auth import get_user_model

from pizzalabapp.models import Ingredient, Order, OrderItem, Pizza

# Model setup functions

def setup_return_order():
    ingredient = Ingredient.objects.create(name='AutoIngredient')
    pizza = Pizza.objects.create(name="AutoPizza", price=10)
    pizza.ingredients.add(ingredient)

    user = get_user_model().objects.create(
        username="testuser",
        password="testpassword",
        email="test@email.com"
    )
    order = Order.objects.create(
        payment_method="CASH",
        delivery_address="Home",
        customer=user
    )
    OrderItem.objects.create(
        quantity=5,
        pizza=pizza,
        order=order
    )
    order.calculate_total_price()
    order.save()

    return order


def setup_pizzas(no_of_pizzas, has_allergens=False, has_lactose=False):
    number_of_pizzas = no_of_pizzas
    number_of_ingredients = 3

    for ingr_id in range(number_of_ingredients):
        Ingredient.objects.create(
            name=f'Ingredient {ingr_id}',
            is_allergen=has_allergens,
            has_lactose=has_lactose
        )

    for pizza_id in range(number_of_pizzas):
        pizza = Pizza.objects.create(
            name=f'Pizza {pizza_id}',
            price=pizza_id + 10
        )
        pizza.ingredients.set(Ingredient.objects.all())
