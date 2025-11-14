from django.db import models
from django.conf import settings

class Propiedad(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='propiedades'
    )
    departamento = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    activa = models.BooleanField(default=True)

    def __str__(self):
        nombre = self.usuario.get_full_name() if hasattr(self.usuario, 'get_full_name') else str(self.usuario)
        return f"{self.direccion}, {self.ciudad} ({nombre})"
