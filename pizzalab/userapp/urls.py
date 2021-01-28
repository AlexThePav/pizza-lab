from django.urls import include, path
from rest_framework.routers import DefaultRouter

from userapp import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]