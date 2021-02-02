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


class PizzaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
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


class OrderItemListSerializer(serializers.ModelSerializer):
    pizza = PizzaListSerializer()

    class Meta:
        model = OrderItem
        fields = ('pizza', 'quantity')

    def validate_pizza(self, value):
        pizza_name = value.get('name')
        try:
            Pizza.objects.get(name=pizza_name)
        except Pizza.DoesNotExist:
            raise serializers.ValidationError(
                f"Pizza with name '{pizza_name}' does not exist"
            )


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemListSerializer(many=True)
    customer = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'total_price': {'read_only': True}
        }

    def create(self, validated_data):
        initial_order_items_data = self.initial_data.get('order_items')
        validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item in initial_order_items_data:
            order_item = OrderItem.objects.create(
                pizza=Pizza.objects.get(name=item.get('pizza').get('name')),
                quantity=item.get('quantity'),
                order=order
            )
            order.order_items.add(order_item)
        order.total_price = order.get_total_price()
        order.save()

        return order
