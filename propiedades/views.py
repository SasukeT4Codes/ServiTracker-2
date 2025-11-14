from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Propiedad
from .forms import PropiedadForm

# 📋 Listar propiedades del usuario
@login_required
def lista_propiedades(request):
    propiedades = Propiedad.objects.filter(usuario=request.user)
    return render(request, 'propiedades/lista.html', {'propiedades': propiedades})

# ➕ Crear nueva propiedad
@login_required
def crear_propiedad(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST)
        if form.is_valid():
            propiedad = form.save(commit=False)
            propiedad.usuario = request.user
            propiedad.save()
            return redirect('lista_propiedades')
    else:
        form = PropiedadForm()
    return render(request, 'propiedades/crear.html', {'form': form})

# ✏️ Editar propiedad existente
@login_required
def editar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = PropiedadForm(request.POST, instance=propiedad)
        if form.is_valid():
            form.save()
            return redirect('lista_propiedades')
    else:
        form = PropiedadForm(instance=propiedad)
    return render(request, 'propiedades/editar.html', {'form': form})

# ❌ Eliminar propiedad
@login_required
def eliminar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk, usuario=request.user)
    if request.method == 'POST':
        propiedad.delete()
        return redirect('lista_propiedades')
    return render(request, 'propiedades/eliminar.html', {'propiedad': propiedad})
