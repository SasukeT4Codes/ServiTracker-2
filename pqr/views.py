from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PQR, EstadoPQR
from .forms import PQRForm

# 📋 Listar PQR del usuario
@login_required
def lista_pqr(request):
    pqr_list = PQR.objects.filter(ciudadano=request.user)
    return render(request, 'pqr/lista.html', {'pqr_list': pqr_list})

# ➕ Crear nuevo PQR
@login_required
def crear_pqr(request):
    if request.method == 'POST':
        form = PQRForm(request.POST)
        if form.is_valid():
            pqr = form.save(commit=False)
            pqr.ciudadano = request.user
            # Estado inicial: Pendiente
            estado_pendiente = EstadoPQR.objects.get(nombre="Pendiente")
            pqr.estado = estado_pendiente
            pqr.save()
            return redirect('lista_pqr')
    else:
        form = PQRForm()
    return render(request, 'pqr/crear.html', {'form': form})

# ✏️ Editar PQR (solo si está pendiente)
@login_required
def editar_pqr(request, pk):
    pqr = get_object_or_404(PQR, pk=pk, ciudadano=request.user)
    if pqr.estado.nombre != "Pendiente":
        return redirect('lista_pqr')  # no se puede editar si ya está en curso o resuelto
    if request.method == 'POST':
        form = PQRForm(request.POST, instance=pqr)
        if form.is_valid():
            form.save()
            return redirect('lista_pqr')
    else:
        form = PQRForm(instance=pqr)
    return render(request, 'pqr/editar.html', {'form': form})

# ❌ Eliminar PQR (solo si está pendiente)
@login_required
def eliminar_pqr(request, pk):
    pqr = get_object_or_404(PQR, pk=pk, ciudadano=request.user)
    if pqr.estado.nombre != "Pendiente":
        return redirect('lista_pqr')
    if request.method == 'POST':
        pqr.delete()
        return redirect('lista_pqr')
    return render(request, 'pqr/eliminar.html', {'pqr': pqr})
