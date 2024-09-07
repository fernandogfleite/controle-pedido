from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.apps.order.views import order

app_name = "order"

router = DefaultRouter()

router.register(r"tables", order.TableViewSet)
router.register(r"ingredients", order.IngredientViewSet)
router.register(r"dishes", order.DishViewSet)
router.register(r"orders", order.OrderViewSet)
router.register(r"ingredient-dishes", order.IngredientDishViewSet)
router.register(r"order-dishes", order.OrderDishViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
