from rest_framework import serializers

from pizzalabapp.models import Ingredient, Order, OrderItem, Pizza


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name',)
        extra_kwargs = {'name': {'validators': []}}


class PizzaSerializer(serializers.HyperlinkedModelSerializer):
    ingredients = IngredientListSerializer(many=True)
    has_allergen_ingredients = serializers.SerializerMethodField()
    has_lactose_ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Pizza
        fields = '__all__'

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        pizza = Pizza.objects.create(**validated_data)
        for ingredient in ingredients_data:
            pizza.ingredients.add(
                Ingredient.objects.get(name=ingredient.get('name'))
            )

        return pizza

    def validate_ingredients(self, value):
        for ingredient in value:
            ingr_name = ingredient.get('name')
            try:
                Ingredient.objects.get(name=ingr_name)
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    "Ingredient with name '{}' does not exist".format(ingr_name)
                )

        return value

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
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
