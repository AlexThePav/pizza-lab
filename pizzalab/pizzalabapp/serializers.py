from rest_framework import serializers

from pizzalabapp.models import Pizza, Ingredient, Order, OrderItem


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name',)


class PizzaSerializer(serializers.HyperlinkedModelSerializer):
    ingredients = IngredientListSerializer(many=True)
    has_allergen_ingredients = serializers.SerializerMethodField()
    has_lactose_ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Pizza
        fields = '__all__'

    def get_has_allergen_ingredients(self, instance):
        for ingredient in instance.ingredients.all():
            if ingredient.is_allergen:
                return True
        return False

    def get_has_lactose_ingredients(self, instance):
        for ingredient in instance.ingredients.all():
            if ingredient.has_lactose:
                return True
        return False


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orders = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
