# usuarios/models.py
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
        return self.create_user(documento, password, **extra_fields)

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

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "documento"
    REQUIRED_FIELDS = []  # email, nombres, etc., si los quisieras obligatorios

    def __str__(self):
        return self.get_full_name() or self.documento

    def get_full_name(self):
        nombre = (self.nombres or "").strip()
        apellido = (self.apellidos or "").strip()
        full = f"{nombre} {apellido}".strip()
        return full or ""
