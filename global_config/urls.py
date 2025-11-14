from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('usuarios/', include('usuarios.urls')),
    path('propiedades/', include('propiedades.urls')),
    path('pqr/', include('pqr.urls')),
    path('reportes/', include('reportes.urls')),

]
