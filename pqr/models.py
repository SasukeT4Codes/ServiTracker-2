from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from propiedades.models import Propiedad


class TipoFalla(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class EstadoPQR(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


# Registro interno para “usuarios insistentes” (intentan crear >3 PQR activas en la misma propiedad)
class UsuarioInsistente(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    total_activas_en_intento = models.PositiveIntegerField(default=0)
    fecha_intento = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Usuario insistente"
        verbose_name_plural = "Usuarios insistentes"
        ordering = ["-fecha_intento"]

    def __str__(self):
        return f"{self.usuario} intentó crear más PQR en {self.propiedad} (activas: {self.total_activas_en_intento})"


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

    # 🔄 Campos para PQR rápido (cuando no hay propiedad registrada)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=20, unique=True, null=True, blank=True)

    tipo_falla = models.ForeignKey(TipoFalla, on_delete=models.PROTECT)
    descripcion = models.TextField()
    estado = models.ForeignKey(EstadoPQR, on_delete=models.PROTECT)

    tecnico_asignado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pqrs_tecnico"
    )
    agente_revisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pqrs_agente"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PQR #{self.id} - {self.tipo_falla.nombre} ({self.estado.nombre})"

    def clean(self):
        # Validar que exista ciudadano y propiedad para aplicar la regla de máximo 3 activas
        if self.ciudadano and self.propiedad:
            estados_activos = ["Pendiente", "En curso", "Urgente", "Muy urgente"]
            qs = PQR.objects.filter(
                ciudadano=self.ciudadano,
                propiedad=self.propiedad,
                estado__nombre__in=estados_activos
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)

            activas = qs.count()
            if activas >= 3:
                UsuarioInsistente.objects.create(
                    usuario=self.ciudadano,
                    propiedad=self.propiedad,
                    total_activas_en_intento=activas
                )
                raise ValidationError("No puedes tener más de 3 PQR activas para la misma propiedad.")

        # Validar que el teléfono de contacto sea único si se usa
        if self.telefono_contacto:
            if PQR.objects.filter(telefono_contacto=self.telefono_contacto).exclude(pk=self.pk).exists():
                raise ValidationError("Este número de teléfono ya está registrado en otro PQR.")

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
