from django import forms
from .models import PQR
from usuarios.models import Usuario

# Formulario para ciudadanos: crear/editar PQR normal
class PQRForm(forms.ModelForm):
    class Meta:
        model = PQR
        fields = ['propiedad', 'tipo_falla', 'descripcion']
        widgets = {
            'propiedad': forms.Select(attrs={'class': 'form-select'}),
            'tipo_falla': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


# Formulario para PQR rápido (anónimo, con dirección y teléfono)
class PQRAnonimoForm(forms.ModelForm):
    class Meta:
        model = PQR
        fields = ['departamento', 'ciudad', 'direccion', 'tipo_falla', 'descripcion', 'telefono_contacto']
        widgets = {
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_falla': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_telefono_contacto(self):
        telefono = self.cleaned_data["telefono_contacto"]
        if PQR.objects.filter(telefono_contacto=telefono).exists():
            raise forms.ValidationError("Este número de teléfono ya está registrado en otro PQR.")
        return telefono


# Formulario para agentes/administradores: asignar técnico a un PQR
class AsignarTecnicoForm(forms.ModelForm):
    tecnico_asignado = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(rol="tecnico"),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = PQR
        fields = ['tecnico_asignado']


# Formulario para administradores: asignar agente a un PQR
class AsignarAgenteForm(forms.Form):
    agente = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(rol="agente"),
        required=True,
        label="Seleccionar agente",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
