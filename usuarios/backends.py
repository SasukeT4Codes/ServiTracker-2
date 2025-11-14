# usuarios/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class DocumentoBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 'username' viene del formulario estándar, lo usamos como documento
        documento = kwargs.get('documento') or username
        try:
            user = Usuario.objects.get(documento=documento)
        except Usuario.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
