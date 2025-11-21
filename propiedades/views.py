from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Propiedad
from .forms import PropiedadForm

# 📋 Listar todas las propiedades (solo admin/staff)
@user_passes_test(lambda u: u.is_staff or u.rol == "administrador")
def lista_propiedades(request):
    propiedades = Propiedad.objects.all()
    return render(request, 'propiedades/propiedades.html', {'propiedades': propiedades})

# ➕ Crear nueva propiedad (solo admin/staff)
@user_passes_test(lambda u: u.is_staff or u.rol == "administrador")
def crear_propiedad(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_propiedades')
    else:
        form = PropiedadForm()
    return render(request, 'propiedades/crear.html', {'form': form})

# ✏️ Editar propiedad existente (solo admin/staff)
@user_passes_test(lambda u: u.is_staff or u.rol == "administrador")
def editar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        form = PropiedadForm(request.POST, instance=propiedad)
        if form.is_valid():
            form.save()
            return redirect('lista_propiedades')
    else:
        form = PropiedadForm(instance=propiedad)
    return render(request, 'propiedades/editar.html', {'form': form, 'propiedad': propiedad})

# ❌ Eliminar propiedad (solo admin/staff)
@user_passes_test(lambda u: u.is_staff or u.rol == "administrador")
def eliminar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        propiedad.delete()
        return redirect('lista_propiedades')
    return render(request, 'propiedades/eliminar.html', {'propiedad': propiedad})
