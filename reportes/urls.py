from django.urls import path
from . import views

urlpatterns = [
    path("admin/", views.dashboard_admin, name="dashboard_admin"),
    path("agente/", views.dashboard_agente, name="dashboard_agente"),
    path("tecnico/", views.dashboard_tecnico, name="dashboard_tecnico"),
    path("todas/", views.lista_todas_pqr, name="lista_todas_pqr"),
]
