from django.urls import path
from . import views

urlpatterns = [
    # Página principal y autenticación
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Registro público (usuarios anónimos crean su propia cuenta)
    path("registro/", views.registro, name="registro"),

    # Perfil y cambio de contraseña (usuario autenticado)
    path("perfil/", views.perfil, name="perfil"),
    path("perfil/cambiar-contrasena/", views.cambiar_contrasena, name="cambiar_contrasena"),

    # Gestión interna de usuarios (solo admin/staff)
    path("usuarios/lista/", views.lista_usuarios, name="lista_usuarios"),
    path("usuarios/nuevo/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/editar/<int:pk>/", views.editar_usuario, name="editar_usuario"),

    # Dashboard del ciudadano
    path("dashboard/", views.dashboard_ciudadano, name="dashboard_ciudadano"),
]
