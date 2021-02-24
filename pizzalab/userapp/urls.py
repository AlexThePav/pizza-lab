from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_views

from userapp import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/', token_views.obtain_auth_token)
]