from django.contrib import admin
from .models import PQR, TipoFalla, EstadoPQR

@admin.register(TipoFalla)
class TipoFallaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)

@admin.register(EstadoPQR)
class EstadoPQRAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)

@admin.register(PQR)
class PQRAdmin(admin.ModelAdmin):
    list_display = ("id", "ciudadano", "propiedad", "tipo_falla", "estado", "tecnico_asignado", "fecha_creacion")
    search_fields = ("descripcion", "ciudadano__username", "propiedad__direccion")
    list_filter = ("estado", "tipo_falla", "propiedad__ciudad")
