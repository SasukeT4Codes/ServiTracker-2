from django.urls import path
from . import views

urlpatterns = [
    # 📋 Listas separadas
    path('mis/', views.mi_lista_pqr, name='mi_lista_pqr'),                # Ciudadano: solo sus PQR
    path('admin/', views.lista_pqr_admin, name='lista_pqr_admin'),        # Admin/Agente: todos los PQR

    # ➕ Crear nuevo PQR (ciudadano)
    path('nuevo/', views.nuevo_pqr, name='nuevo_pqr'),

    # ✏️ Editar / ❌ Eliminar (ciudadano, solo si pendiente)
    path('<int:pk>/editar/', views.editar_pqr, name='editar_pqr'),
    path('<int:pk>/eliminar/', views.eliminar_pqr, name='eliminar_pqr'),

    # 🔧 Técnico: ver sus asignaciones
    path('mis-asignaciones/', views.mis_asignaciones, name='mis_asignaciones'),

    # 🛠️ Agente/Admin: asignar técnico
    path('<int:pk>/asignar-tecnico/', views.asignar_tecnico, name='asignar_tecnico'),
]
