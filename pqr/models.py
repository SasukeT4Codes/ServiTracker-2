from django.db import models
from django.conf import settings
from propiedades.models import Propiedad

class TipoFalla(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class EstadoPQR(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class PQR(models.Model):
    ciudadano = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="pqr_ciudadano")
    propiedad = models.ForeignKey(Propiedad, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_falla = models.ForeignKey(TipoFalla, on_delete=models.CASCADE)
    descripcion = models.TextField()
    estado = models.ForeignKey(EstadoPQR, on_delete=models.CASCADE)
    tecnico_asignado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pqr_asignados"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PQR {self.id} - {self.tipo_falla.nombre} ({self.estado.nombre})"
