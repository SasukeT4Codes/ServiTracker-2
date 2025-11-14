from django.contrib import admin
from .models import Propiedad

@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    list_display = ("id", "direccion", "ciudad", "usuario")
    search_fields = ("direccion", "ciudad")
    list_filter = ("ciudad",)
