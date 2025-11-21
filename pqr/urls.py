from django.urls import path
from . import views

urlpatterns = [
    # 📋 Listas separadas
    path('mis/', views.mi_lista_pqr, name='mi_lista_pqr'),                # Ciudadano: solo sus PQR
    path('admin/', views.lista_pqr_admin, name='lista_pqr_admin'),        # Admin/Agente: todos los PQR

    # ➕ Crear nuevo PQR (ciudadano)
    path('nuevo/', views.nuevo_pqr, name='nuevo_pqr'),

    # ✏️ Editar (ciudadano, solo si pendiente)
    path('<int:pk>/editar/', views.editar_pqr, name='editar_pqr'),

    # 🔧 Técnico: ver sus asignaciones
    path('mis-asignaciones/', views.mis_asignaciones, name='mis_asignaciones'),

    # 🛠️ Agente/Admin: asignar técnico
    path('<int:pk>/asignar-tecnico/', views.asignar_tecnico, name='asignar_tecnico'),

    # ✅ Cerrar/Resolver PQR (técnico/agente/admin)
    path('<int:pk>/cerrar/', views.cerrar_pqr, name='cerrar_pqr'),

    # Ver los detalles del pqr
    path('<int:pk>/detalle/', views.detalle_pqr, name='detalle_pqr'),

]
