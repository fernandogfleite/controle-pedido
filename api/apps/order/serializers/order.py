from rest_framework import serializers

from api.apps.order.models.order import (
    Dish,
    Ingredient,
    IngredientDish,
    Order,
    OrderDish,
    Table,
)
from api.apps.order.serializers.fields.order import (
    CustomChoiceField,
    DishField,
    IngredientField,
    OrderField,
)


class TableSerializer(serializers.ModelSerializer):
    status = CustomChoiceField(choices=Table.STATUS_CHOICES)

    class Meta:
        model = Table
        fields = ("id", "number", "status", "description")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "description",
        )


class DishSerializer(serializers.ModelSerializer):
    ingredients = IngredientField(many=True, read_only=True)

    class Meta:
        model = Dish
        fields = ("id", "name", "description", "status", "price")

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        ingredients = Ingredient.objects.filter(
            id__in=IngredientDish.objects.filter(dish=instance).values_list(
                "ingredient_id", flat=True
            )
        ).order_by("name")

        representation["ingredients"] = IngredientSerializer(
            ingredients, many=True
        ).data

        return representation

    def create(self, validated_data):
        client_id = self.context["request"].auth.get("client_id")

        ingredients = validated_data.pop("ingredients")

        instance = Dish.objects.create_dish(
            client_id=client_id, ingredients=ingredients, **validated_data
        )

        return instance


class IngredientDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientDish
        fields = ("id", "dish", "ingredient")
        extra_kwargs = {
            "dish": {"write_only": True},
            "ingredient": {"write_only": True},
        }


class OrderDishCreateSerializer(serializers.Serializer):
    dish = DishField()
    description = serializers.CharField(required=False)
    quantity = serializers.IntegerField()
    additional_ingredient = IngredientField(many=True, required=False)
    removed_ingredient = IngredientField(many=True, required=False)


class OrderSerializer(serializers.ModelSerializer):
    dishes = OrderDishCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "table",
            "description",
            "dishes",
            "status",
            "created_by",
            "start_preparation",
            "end_preparation",
        ]

    def create(self, validated_data):
        dishes = validated_data.pop("dishes")

        order = Order.objects.create_order(
            dishes=dishes,
            **validated_data,
            client_id=self.context["request"].auth.get("client_id")
        )

        return order


class OrderDishSerializer(serializers.ModelSerializer):
    order = OrderField()
    dish = DishField()
    additional_ingredient = IngredientSerializer(many=True)
    removed_ingredient = IngredientSerializer(many=True)

    class Meta:
        model = OrderDish
        fields = [
            "id",
            "dish",
            "order",
            "description",
            "quantity",
            "additional_ingredient",
            "removed_ingredient",
        ]
