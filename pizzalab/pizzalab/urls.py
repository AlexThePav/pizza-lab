from django.contrib import admin
from django.urls import include, path

from pizzalabapp import urls as pizzalab_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(pizzalab_urls))
]
