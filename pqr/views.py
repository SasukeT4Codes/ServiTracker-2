from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import PQR, EstadoPQR, Propiedad, TipoFalla
from .forms import PQRForm, AsignarTecnicoForm, AsignarAgenteForm

Usuario = get_user_model()

# 📋 Listar PQR del ciudadano (con paginación)
@login_required
def mi_lista_pqr(request):
    pqr_queryset = PQR.objects.filter(ciudadano=request.user).order_by("-id")
    paginator = Paginator(pqr_queryset, 10)  # 10 PQR por página
    page_number = request.GET.get("page")
    pqr_list = paginator.get_page(page_number)
    return render(request, 'pqr/mis_pqr.html', {'pqr_list': pqr_list})

# 📋 Listar todos los PQR (solo admin/agente, con paginación)
@user_passes_test(lambda u: u.rol in ["agente", "administrador"])
def lista_pqr_admin(request):
    pqr_queryset = PQR.objects.all().order_by("-id")
    for pqr in pqr_queryset:
        pqr.actualizar_estado_urgencia()

    paginator = Paginator(pqr_queryset, 20)  # 20 PQR por página
    page_number = request.GET.get("page")
    pqr_list = paginator.get_page(page_number)

    return render(request, 'pqr/lista.html', {'pqr_list': pqr_list})

# ➕ Crear nuevo PQR (ciudadano)
@login_required
def nuevo_pqr(request):
    if request.method == 'POST':
        form = PQRForm(request.POST)
        form.fields['propiedad'].queryset = Propiedad.objects.filter(usuario=request.user)
        if form.is_valid():
            pqr = form.save(commit=False)
            pqr.ciudadano = request.user
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

# 🔧 Vista para técnicos: Mis asignaciones (con paginación)
@login_required
def mis_asignaciones(request):
    if request.user.rol != "tecnico":
        return redirect('index')
    asignaciones_queryset = PQR.objects.filter(tecnico_asignado=request.user).order_by("-id")
    paginator = Paginator(asignaciones_queryset, 10)  # 10 asignaciones por página
    page_number = request.GET.get("page")
    asignaciones = paginator.get_page(page_number)
    return render(request, 'pqr/mis_asignaciones.html', {'asignaciones': asignaciones})

# 🛠️ Asignar técnico
@login_required
def asignar_tecnico(request, pk):
    if request.user.rol not in ["agente", "administrador"]:
        return redirect('index')
    pqr = get_object_or_404(PQR, pk=pk)
    if request.method == 'POST':
        form = AsignarTecnicoForm(request.POST, instance=pqr)
        if form.is_valid():
            pqr = form.save(commit=False)
            estado_en_curso = EstadoPQR.objects.get(nombre="En curso")
            pqr.estado = estado_en_curso
            pqr.save()
            return redirect('dashboard_admin' if request.user.rol == "administrador" else 'dashboard_agente')
    else:
        form = AsignarTecnicoForm(instance=pqr)
    return render(request, 'pqr/asignar_tecnico.html', {'form': form, 'pqr': pqr})

# 🛠️ Asignar agente (solo admin)
@login_required
def asignar_agente(request, pk):
    if request.user.rol != "administrador":
        return redirect('index')
    pqr = get_object_or_404(PQR, pk=pk)
    if request.method == "POST":
        form = AsignarAgenteForm(request.POST)
        if form.is_valid():
            agente = form.cleaned_data["agente"]
            pqr.agente_asignado = agente
            pqr.save()
            return redirect("dashboard_admin")
    else:
        form = AsignarAgenteForm()
    return render(request, "pqr/asignar_agente.html", {"pqr": pqr, "form": form})

# ✏️ Editar estado del PQR
@login_required
@user_passes_test(lambda u: u.rol in ["agente", "administrador"])
def editar_estado_pqr(request, pk):
    pqr = get_object_or_404(PQR, pk=pk)
    if request.method == "POST":
        nuevo_estado_id = request.POST.get("estado")
        if nuevo_estado_id:
            nuevo_estado = get_object_or_404(EstadoPQR, pk=nuevo_estado_id)
            pqr.estado = nuevo_estado
            pqr.save()
        return redirect("detalle_pqr", pk=pqr.pk)
    estados = EstadoPQR.objects.all()
    return render(request, "pqr/detalle_pqr.html", {
        "pqr": pqr,
        "estados": estados,
    })

# ✅ Cerrar PQR
@login_required
def cerrar_pqr(request, pk):
    if request.user.rol not in ["tecnico", "agente", "administrador"]:
        return redirect('index')
    pqr = get_object_or_404(PQR, pk=pk)
    if request.method == 'POST':
        estado_resuelto = EstadoPQR.objects.get(nombre="Resuelto")
        pqr.estado = estado_resuelto
        pqr.save()
        if request.user.rol == "tecnico":
            return redirect('mis_asignaciones')
        elif request.user.rol == "agente":
            return redirect('lista_pqr_admin')
        else:
            return redirect('dashboard_admin')
    return render(request, 'pqr/cerrar.html', {'pqr': pqr})


# 📋 Detalle de PQR
@login_required
@user_passes_test(lambda u: u.rol in ["agente", "administrador", "tecnico"])
def detalle_pqr(request, pk):
    pqr = get_object_or_404(PQR, pk=pk)
    # Actualizar urgencia si corresponde
    if pqr.estado.nombre in ["Pendiente", "Urgente", "Muy urgente"]:
        try:
            pqr.actualizar_estado_urgencia()
        except Exception:
            pass

    # Solo agentes y administradores pueden ver lista de estados para cambiar
    estados = EstadoPQR.objects.all() if request.user.rol in ["agente", "administrador"] else []

    return render(request, 'pqr/detalle_pqr.html', {
        'pqr': pqr,
        'estados': estados,
    })
