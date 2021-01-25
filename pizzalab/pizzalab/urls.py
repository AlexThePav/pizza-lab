from django.contrib import admin
from django.urls import path, include

from pizzalabapp import urls as pizzalab_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(pizzalab_urls))
]
