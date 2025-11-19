from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm
from .models import Especialidad
from propiedades.models import Propiedad

Usuario = get_user_model()

# 📝 Formulario de registro público (dinámico según rol)
class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Campos adicionales dinámicos
    direccion = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    especialidad = forms.ModelChoiceField(
        queryset=Especialidad.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    nueva_especialidad = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = ['documento', 'nombres', 'apellidos', 'email', 'rol']
        widgets = {
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

            # Si es técnico → asignar especialidad
            if user.rol == "tecnico":
                if self.cleaned_data.get("nueva_especialidad"):
                    esp, _ = Especialidad.objects.get_or_create(nombre=self.cleaned_data["nueva_especialidad"])
                    user.especialidad = esp
                    user.save(update_fields=["especialidad"])
                elif self.cleaned_data.get("especialidad"):
                    user.especialidad = self.cleaned_data["especialidad"]
                    user.save(update_fields=["especialidad"])

            # Si es ciudadano → crear propiedad inicial
            if user.rol == "ciudadano" and self.cleaned_data.get("direccion"):
                Propiedad.objects.create(
                    usuario=user,
                    direccion=self.cleaned_data["direccion"],
                    ciudad="Por definir",
                    departamento="Por definir"
                )

        return user


# 🔐 Formulario de login por documento
class LoginForm(forms.Form):
    documento = forms.CharField(label="Documento", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self._user = None

    def clean(self):
        cleaned = super().clean()
        doc = cleaned.get('documento')
        pwd = cleaned.get('password')
        user = authenticate(self.request, documento=doc, password=pwd)
        if user is None:
            raise forms.ValidationError("Documento o contraseña inválidos.")
        self._user = user
        return cleaned

    def get_user(self):
        return self._user


# 🛠️ Formulario para editar usuarios en el admin
class UsuarioChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Hash de contraseña", help_text="El hash actual de la contraseña.")
    nueva_contrasena = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Si deseas cambiar la contraseña de este usuario, ingrésala aquí."
    )

    class Meta:
        model = Usuario
        fields = (
            "documento",
            "nombres",
            "apellidos",
            "email",
            "rol",
            "especialidad",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
        )

    def clean_password(self):
        # Mantener el hash original si no se cambia
        return self.initial.get("password")


# 🛠️ Formulario para crear usuarios desde el admin
class UsuarioAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = ("documento", "nombres", "apellidos", "email", "rol", "especialidad")

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# 🔑 Formulario para cambiar contraseña (usuario autenticado)
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
