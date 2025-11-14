from django.db import models
from django.conf import settings

class Propiedad(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='propiedades')
    departamento = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.direccion}, {self.ciudad} ({self.usuario.username})"
