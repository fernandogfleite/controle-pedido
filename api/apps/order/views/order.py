from rest_framework import permissions
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.apps.authentication.auth import ClientJWTAuthentication
from api.apps.authentication.mixins import ClientMixin
from api.apps.order.models.order import (
    Dish,
    Ingredient,
    IngredientDish,
    Order,
    OrderDish,
    Table,
)
from api.apps.order.serializers.order import (
    DishSerializer,
    IngredientDishSerializer,
    IngredientSerializer,
    OrderDishSerializer,
    OrderSerializer,
    TableSerializer,
)


class TableViewSet(ClientMixin, ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class IngredientViewSet(ClientMixin, ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class DishViewSet(ClientMixin, ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class IngredientDishViewSet(
    ClientMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = IngredientDish.objects.all()
    serializer_class = IngredientDishSerializer


class OrderViewSet(ClientMixin, ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDishViewSet(ClientMixin, ModelViewSet):
    queryset = OrderDish.objects.all()
    serializer_class = OrderDishSerializer
