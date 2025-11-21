from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from .models import PQR, EstadoPQR, Propiedad, TipoFalla
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
    # actualizar estados urgentes
    for pqr in pqr_list:
        pqr.actualizar_estado_urgencia()
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

# 🔧 Vista para técnicos: Mis asignaciones
@login_required
def mis_asignaciones(request):
    if request.user.rol != "tecnico":
        return redirect('index')
    asignaciones = PQR.objects.filter(tecnico_asignado=request.user)
    return render(request, 'pqr/mis_asignaciones.html', {'asignaciones': asignaciones})

# 🛠️ Vista para agentes/administradores: asignar técnico a un PQR
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
            if request.user.rol == "agente":
                return redirect('dashboard_agente')
            else:
                return redirect('dashboard_admin')
    else:
        form = AsignarTecnicoForm(instance=pqr)
    return render(request, 'pqr/asignar_tecnico.html', {'form': form, 'pqr': pqr})

# ✅ Cerrar/Resolver PQR (técnico/agente/admin)
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

# 📊 Dashboard Administrador
@user_passes_test(lambda u: u.rol == "administrador")
def dashboard_admin(request):
    pendientes = PQR.objects.filter(estado__nombre="Pendiente").count()
    en_curso = PQR.objects.filter(estado__nombre="En curso").count()
    resueltos = PQR.objects.filter(estado__nombre="Resuelto").count()

    # estadísticas por ciudad
    estadisticas_ciudad = {}
    ciudades = Propiedad.objects.values("ciudad").distinct()
    for c in ciudades:
        ciudad = c["ciudad"]
        estadisticas_ciudad[ciudad] = {
            "pendientes": PQR.objects.filter(propiedad__ciudad=ciudad, estado__nombre="Pendiente").count(),
            "resueltos": PQR.objects.filter(propiedad__ciudad=ciudad, estado__nombre="Resuelto").count(),
        }

    # filtros
    ciudad = request.GET.get("ciudad", "")
    tipo_falla_id = request.GET.get("tipo_falla", "")
    pqr_pendientes = PQR.objects.filter(estado__nombre="Pendiente")
    if ciudad:
        pqr_pendientes = pqr_pendientes.filter(propiedad__ciudad__icontains=ciudad)
    if tipo_falla_id:
        pqr_pendientes = pqr_pendientes.filter(tipo_falla_id=tipo_falla_id)

    tipos_falla = TipoFalla.objects.all()

    return render(request, "pqr/dashboard_admin.html", {
        "pendientes": pendientes,
        "en_curso": en_curso,
        "resueltos": resueltos,
        "estadisticas_ciudad": estadisticas_ciudad,
        "pqr_pendientes": pqr_pendientes,
        "ciudad": ciudad,
        "tipo_falla_id": tipo_falla_id,
        "tipos_falla": tipos_falla,
    })

# 📋 Detalle de PQR
@login_required
@user_passes_test(lambda u: u.rol in ["agente", "administrador", "tecnico"])
def detalle_pqr(request, pk):
    pqr = get_object_or_404(PQR, pk=pk)
    # actualizar urgencia al entrar
    if pqr.estado.nombre in ["Pendiente", "Urgente", "Muy urgente"]:
        try:
            pqr.actualizar_estado_urgencia()
        except Exception:
            pass
    return render(request, 'pqr/detalle_pqr.html', {'pqr': pqr})
