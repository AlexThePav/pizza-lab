from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pizzalabapp import views

router = DefaultRouter()
router.register(r'pizzas', views.PizzaViewSet, basename="pizza")
router.register(r'ingredients', views.IngredientViewSet, basename="ingredient")
router.register(r'orders', views.OrderViewSet, basename="order")
router.register(r'order_items', views.OrderItemViewSet, basename="order_item")

urlpatterns = [
    path('', include(router.urls)),
]
