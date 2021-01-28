from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pizzalabapp.urls')),
    path('', include('userapp.urls')),
    path('auth/', include('rest_framework.urls'))
]
