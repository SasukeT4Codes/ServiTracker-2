from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, documento, password=None, **extra_fields):
        if not documento:
            raise ValueError("El documento es obligatorio")
        user = self.model(documento=documento, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, documento, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'administrador')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(documento, password, **extra_fields)


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ("administrador", "Administrador"),
        ("agente", "Agente"),
        ("tecnico", "Técnico"),
        ("ciudadano", "Ciudadano"),
    ]

    documento = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    nombres = models.CharField(max_length=100, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLES, default="ciudadano")

    # Relación opcional para técnicos
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "documento"
    REQUIRED_FIELDS = []  # puedes agregar 'email' si quieres que sea obligatorio

    def __str__(self):
        return self.get_public_name()

    def get_full_name(self):
        nombre = (self.nombres or "").strip()
        apellido = (self.apellidos or "").strip()
        full = f"{nombre} {apellido}".strip()
        return full or ""

    def get_public_name(self):
        return self.get_full_name() or "Usuario"
