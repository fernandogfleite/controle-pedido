from collections import OrderedDict

from rest_framework import serializers

from api.apps.order.models.order import Dish, Ingredient, Order


class ModifiedRelatedField(serializers.RelatedField):
    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([(item.pk, self.display_value(item)) for item in queryset])


class SaasRelatedField(ModifiedRelatedField):
    def get_queryset(self):
        self.client_id = self.context["request"].auth.get("client_id")

        return self.model.objects.filter(client_id=self.client_id)

    def to_internal_value(self, data):
        try:
            return self.get_queryset.objects.get(id=data)

        except self.model.DoesNotExist:
            raise serializers.ValidationError("Invalid ID")


class IngredientField(SaasRelatedField):
    model = Ingredient

    def to_representation(self, value):
        return {
            "id": value.id,
            "name": value.name,
            "description": value.description,
        }


class DishField(SaasRelatedField):
    model = Dish

    def to_representation(self, value):
        return {
            "id": value.id,
            "name": value.name,
            "description": value.description,
            "price": value.price,
        }


class OrderField(SaasRelatedField):
    model = Order

    def to_representation(self, value):
        return {
            "id": value.id,
            "table": value.table,
            "description": value.description,
            "created_by": value.created_by,
        }
