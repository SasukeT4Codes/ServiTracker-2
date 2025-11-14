from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # raíz del sitio
    path('propiedades/', include('propiedades.urls')),
    path('pqr/', include('pqr.urls')),
    path('reportes/', include('reportes.urls')),

]
