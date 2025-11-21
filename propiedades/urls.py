from django.urls import path
from . import views

urlpatterns = [
    # Listado global (admin/staff)
    path('', views.lista_propiedades, name='lista_propiedades'),

    # Listado propio (ciudadano)
    path('mis/', views.mis_propiedades, name='mis_propiedades'),

    # CRUD admin/staff
    path('crear/', views.crear_propiedad, name='crear_propiedad'),
    path('<int:pk>/editar/', views.editar_propiedad, name='editar_propiedad'),
    path('<int:pk>/eliminar/', views.eliminar_propiedad, name='eliminar_propiedad'),
]
