from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("perfil/", views.perfil, name="perfil"),

    # Gestión interna de usuarios (solo para admin/agente)
    path("lista/", views.lista_usuarios, name="lista_usuarios"),
    path("nuevo/", views.crear_usuario, name="crear_usuario"),
    path("editar/<int:pk>/", views.editar_usuario, name="editar_usuario"),

    # Cambio de contraseña (usuario autenticado)
    path("perfil/cambiar-contrasena/", views.cambiar_contrasena, name="cambiar_contrasena"),

    path("dashboard/", views.dashboard_ciudadano, name="dashboard_ciudadano"),
]
