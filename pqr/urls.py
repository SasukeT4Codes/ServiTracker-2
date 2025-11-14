from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pqr, name='lista_pqr'),
    path('crear/', views.crear_pqr, name='crear_pqr'),
    path('editar/<int:pk>/', views.editar_pqr, name='editar_pqr'),
    path('eliminar/<int:pk>/', views.eliminar_pqr, name='eliminar_pqr'),
]
