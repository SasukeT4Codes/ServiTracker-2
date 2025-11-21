from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_propiedades, name='lista_propiedades'),
    path('crear/', views.crear_propiedad, name='crear_propiedad'),
    path('<int:pk>/editar/', views.editar_propiedad, name='editar_propiedad'),
    path('<int:pk>/eliminar/', views.eliminar_propiedad, name='eliminar_propiedad'),
]
