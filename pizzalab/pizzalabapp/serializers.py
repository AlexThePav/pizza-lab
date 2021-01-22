from rest_framework import serializers
from django.conf import settings
from rest_framework.reverse import reverse


from pizzalabapp.models import Pizza, Ingredient, Order, OrderItem


class IngredientListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ['name', 'url', ]

    def get_url(self, obj):
        ingredient = reverse('api:ingredient-detail', args=[obj.id])
        return f'http://{settings.BASE_IP}{ingredient}'


class PizzaSerializer(serializers.ModelSerializer):
    ingredients = IngredientListSerializer(many=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Pizza
        fields = '__all__'

    def get_url(self, obj):
        pizza = reverse('api:pizza-detail', args=[obj.id])
        return f'http://{settings.BASE_IP}{pizza}'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orders = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

