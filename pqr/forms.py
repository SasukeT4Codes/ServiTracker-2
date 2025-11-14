from django import forms
from .models import PQR

class PQRForm(forms.ModelForm):
    class Meta:
        model = PQR
        fields = ['propiedad', 'tipo_falla', 'descripcion']
        widgets = {
            'propiedad': forms.Select(attrs={'class': 'form-select'}),
            'tipo_falla': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
