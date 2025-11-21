from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import PQR, EstadoPQR, Propiedad
from .forms import PQRForm, AsignarTecnicoForm

# 📋 Listar PQR del ciudadano
@login_required
def mi_lista_pqr(request):
    pqr_list = PQR.objects.filter(ciudadano=request.user)
    return render(request, 'pqr/mi-lista.html', {'pqr_list': pqr_list})

# 📋 Listar todos los PQR (solo admin/agente)
@user_passes_test(lambda u: u.rol in ["agente", "administrador"])
def lista_pqr_admin(request):
    pqr_list = PQR.objects.all()
    return render(request, 'pqr/lista.html', {'pqr_list': pqr_list})

# ➕ Crear nuevo PQR (ciudadano)
@login_required
def nuevo_pqr(request):
    if request.method == 'POST':
        form = PQRForm(request.POST)
        # Filtrar propiedades del usuario autenticado
        form.fields['propiedad'].queryset = Propiedad.objects.filter(usuario=request.user)
        if form.is_valid():
            pqr = form.save(commit=False)
            pqr.ciudadano = request.user
            # Estado inicial: Pendiente
            estado_pendiente = EstadoPQR.objects.get(nombre="Pendiente")
            pqr.estado = estado_pendiente
            pqr.save()
            return redirect('mi_lista_pqr')
    else:
        form = PQRForm()
        form.fields['propiedad'].queryset = Propiedad.objects.filter(usuario=request.user)
    return render(request, 'pqr/nuevo_pqr.html', {'form': form})

# ✏️ Editar PQR (solo si está pendiente)
@login_required
def editar_pqr(request, pk):
    pqr = get_object_or_404(PQR, pk=pk, ciudadano=request.user)
    if pqr.estado.nombre != "Pendiente":
        return redirect('mi_lista_pqr')
    if request.method == 'POST':
        form = PQRForm(request.POST, instance=pqr)
        if form.is_valid():
            form.save()
            return redirect('mi_lista_pqr')
    else:
        form = PQRForm(instance=pqr)
    return render(request, 'pqr/editar.html', {'form': form})

# ❌ Eliminar PQR (solo si está pendiente)
@login_required
def eliminar_pqr(request, pk):
    pqr = get_object_or_404(PQR, pk=pk, ciudadano=request.user)
    if pqr.estado.nombre != "Pendiente":
        return redirect('mi_lista_pqr')
    if request.method == 'POST':
        pqr.delete()
        return redirect('mi_lista_pqr')
    return render(request, 'pqr/eliminar.html', {'pqr': pqr})

# 🔧 Vista para técnicos: Mis asignaciones
@login_required
def mis_asignaciones(request):
    if request.user.rol != "tecnico":
        return redirect('index')  # solo técnicos pueden entrar
    asignaciones = PQR.objects.filter(tecnico_asignado=request.user)
    return render(request, 'pqr/mis_asignaciones.html', {'asignaciones': asignaciones})

# 🛠️ Vista para agentes/administradores: asignar técnico a un PQR
@login_required
def asignar_tecnico(request, pk):
    if request.user.rol not in ["agente", "administrador"]:
        return redirect('index')  # solo agentes y administradores pueden asignar

    pqr = get_object_or_404(PQR, pk=pk)
    if request.method == 'POST':
        form = AsignarTecnicoForm(request.POST, instance=pqr)
        if form.is_valid():
            pqr = form.save(commit=False)
            # Cambiamos estado a "En curso"
            estado_en_curso = EstadoPQR.objects.get(nombre="En curso")
            pqr.estado = estado_en_curso
            pqr.save()
            # Redirigir según rol
            if request.user.rol == "agente":
                return redirect('dashboard_agente')
            else:
                return redirect('dashboard_admin')
    else:
        form = AsignarTecnicoForm(instance=pqr)
    return render(request, 'pqr/asignar_tecnico.html', {'form': form, 'pqr': pqr})
