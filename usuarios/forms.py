from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate

Usuario = get_user_model()

# 📝 Formulario de registro público
class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

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
    password = ReadOnlyPasswordHashField(label="Hash de contraseña")

    class Meta:
        model = Usuario
        fields = ("documento", "nombres", "apellidos", "email", "rol", "password", "is_active", "is_staff", "is_superuser")

    def clean_password(self):
        return self.initial.get("password")

# 🛠️ Formulario para crear usuarios desde el admin
class UsuarioAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = ("documento", "nombres", "apellidos", "email", "rol")

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
