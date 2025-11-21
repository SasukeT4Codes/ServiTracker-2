from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
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
    ciudadano = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pqrs_ciudadano"
    )
    propiedad = models.ForeignKey(
        Propiedad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tipo_falla = models.ForeignKey(
        TipoFalla,
        on_delete=models.PROTECT
    )
    descripcion = models.TextField()
    estado = models.ForeignKey(
        EstadoPQR,
        on_delete=models.PROTECT
    )
    tecnico_asignado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pqrs_tecnico"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PQR #{self.id} - {self.tipo_falla.nombre} ({self.estado.nombre})"

    def actualizar_estado_urgencia(self):
        if self.estado.nombre == "Pendiente":
            dias = (timezone.now() - self.fecha_creacion).days
            if dias >= 7:
                urgente = EstadoPQR.objects.get(nombre="Muy urgente")
                self.estado = urgente
                self.save()
            elif dias >= 3:
                urgente = EstadoPQR.objects.get(nombre="Urgente")
                self.estado = urgente
                self.save()
