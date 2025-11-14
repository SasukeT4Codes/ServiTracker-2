from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario
from .forms import UsuarioAdminCreationForm, UsuarioChangeForm

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    add_form = UsuarioAdminCreationForm
    form = UsuarioChangeForm
    model = Usuario

    list_display = ("id", "documento", "nombres", "apellidos", "email", "rol", "is_active", "is_staff")
    list_filter = ("rol", "is_active", "is_staff")
    search_fields = ("documento", "nombres", "apellidos", "email")
    ordering = ("documento",)
