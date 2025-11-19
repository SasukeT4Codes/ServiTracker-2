from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    path("dashboard/agente/", views.dashboard_agente, name="dashboard_agente"),
    path("dashboard/tecnico/", views.dashboard_tecnico, name="dashboard_tecnico"),
]
