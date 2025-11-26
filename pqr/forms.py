from django import forms
from .models import PQR
from usuarios.models import Usuario

# Formulario para ciudadanos: crear/editar PQR
class PQRForm(forms.ModelForm):
    class Meta:
        model = PQR
        fields = ['propiedad', 'tipo_falla', 'descripcion']
        widgets = {
            'propiedad': forms.Select(attrs={'class': 'form-select'}),
            'tipo_falla': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

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
