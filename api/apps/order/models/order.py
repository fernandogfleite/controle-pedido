from django.db import models, transaction
from django.utils import timezone

from api.apps.authentication.models.client import Base


class DishManager(models.Manager):
    @transaction.atomic
    def create_dish(self, name, description, price, client, ingredients):
        dish = self.create(
            name=name, description=description, price=price, client=client
        )

        ingredient_dish = [
            IngredientDish(ingredient=ingredient, dish=dish)
            for ingredient in ingredients
        ]

        IngredientDish.objects.bulk_create(ingredient_dish)

        return dish


class OrderManager(models.Manager):
    @transaction.atomic
    def create_order(self, table, client, description, dishes, created_by):
        order = self.create(
            table=table, client=client, description=description, created_by=created_by
        )

        for dish in dishes:
            order_dish = OrderDish.objects.create(
                order=order,
                dish=dish["dish"],
                client=client,
                quantity=dish["quantity"],
                description=dish.get("description", ""),
            )

            if dish.get("additional_ingredient"):
                order_dish.additional_ingredient.add(*dish["additional_ingredient"])

            if dish.get("removed_ingredient"):
                order_dish.removed_ingredient.add(*dish["removed_ingredient"])

        return order


class Table(Base):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"

    STATUS_CHOICES = (
        (AVAILABLE, "Disponível"),
        (UNAVAILABLE, "Indisponível"),
    )

    number = models.IntegerField()
    description = models.TextField()
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=AVAILABLE)
    client = models.ForeignKey("authentication.Client", on_delete=models.PROTECT)

    class Meta:
        db_table = "tables"
        verbose_name = "Table"
        verbose_name_plural = "Tables"
        unique_together = ["number", "client"]

    def __str__(self):
        return f"Table {self.number} - {self.client.name}"


class Ingredient(Base):
    name = models.CharField(max_length=255)
    description = models.TextField()
    client = models.ForeignKey("authentication.Client", on_delete=models.PROTECT)

    class Meta:
        db_table = "ingredients"
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        unique_together = ["name", "client"]

    def __str__(self):
        return self.name


class Dish(Base):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"

    STATUS_CHOICES = (
        (AVAILABLE, "Disponível"),
        (UNAVAILABLE, "Indisponível"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=AVAILABLE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey("authentication.Client", on_delete=models.PROTECT)

    objects = DishManager()

    class Meta:
        db_table = "dishes"
        verbose_name = "Dish"
        verbose_name_plural = "Dishes"
        unique_together = ["name", "client"]

    def __str__(self):
        return self.name


class IngredientDish(Base):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT)

    class Meta:
        db_table = "ingredients_dishes"
        verbose_name = "Ingredient Dish"
        verbose_name_plural = "Ingredients Dishes"

    def __str__(self):
        return f"{self.ingredient.name} - {self.dish.name}"


class Order(Base):
    RECEIVED = "RECEIVED"
    PREPARING = "PREPARING"
    CANCELLED = "CANCELLED"
    DONE = "DONE"

    STATUS_CHOICES = (
        (RECEIVED, "Recebido"),
        (PREPARING, "Preparando"),
        (DONE, "Pronto"),
    )

    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    client = models.ForeignKey("authentication.Client", on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=RECEIVED)
    created_by = models.ForeignKey(
        "authentication.User", on_delete=models.PROTECT, related_name="orders"
    )

    start_preparation = models.DateTimeField(null=True, blank=True)
    end_preparation = models.DateTimeField(null=True, blank=True)

    objects = OrderManager()

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order from {self.table.client.name} - Table {self.table.number}"


class OrderDish(Base):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT)
    client = models.ForeignKey("authentication.Client", on_delete=models.PROTECT)
    quantity = models.IntegerField()
    additional_ingredient = models.ManyToManyField(
        Ingredient, blank=True, related_name="additional_ingredient"
    )
    removed_ingredient = models.ManyToManyField(
        Ingredient, blank=True, related_name="removed_ingredient"
    )
    description = models.TextField(blank=True)

    class Meta:
        db_table = "orders_dishes"
        verbose_name = "Order Dish"
        verbose_name_plural = "Orders Dishes"

    def __str__(self):
        return f"{self.order} - {self.dish.name} - {self.quantity}"


class OrderHistory(Base):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="history")
    client = models.ForeignKey("authentication.Client", on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=Order.STATUS_CHOICES)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    changed_by = models.ForeignKey("authentication.User", on_delete=models.PROTECT)

    class Meta:
        db_table = "orders_history"
        verbose_name = "Order History"
        verbose_name_plural = "Orders History"

    def __str__(self):
        return f"{self.order} - {self.status} - {self.timestamp}"
