from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pqr.models import PQR, TipoFalla

# 📊 Dashboard principal (solo administradores y agentes)
@login_required
def dashboard(request):
    # Solo agentes y administradores
    if request.user.rol not in ["agente", "administrador"]:
        return redirect('index')

    # --- Filtros desde GET ---
    ciudad = request.GET.get("ciudad")
    tipo_falla_id = request.GET.get("tipo_falla")

    # --- Contadores globales ---
    pendientes = PQR.objects.filter(estado__nombre="Pendiente").count()
    en_curso = PQR.objects.filter(estado__nombre="En curso").count()
    resueltos = PQR.objects.filter(estado__nombre="Resuelto").count()

    # --- Estadísticas por ciudad ---
    estadisticas_ciudad = {}
    for pqr in PQR.objects.select_related('propiedad').all():
        if pqr.propiedad:
            ciudad_key = pqr.propiedad.ciudad
            if ciudad_key not in estadisticas_ciudad:
                estadisticas_ciudad[ciudad_key] = {"pendientes": 0, "resueltos": 0}
            if pqr.estado.nombre == "Pendiente":
                estadisticas_ciudad[ciudad_key]["pendientes"] += 1
            elif pqr.estado.nombre == "Resuelto":
                estadisticas_ciudad[ciudad_key]["resueltos"] += 1

    # --- Base queryset de pendientes ---
    pqr_pendientes = PQR.objects.filter(estado__nombre="Pendiente")

    # --- Aplicar filtros ---
    if ciudad:
        pqr_pendientes = pqr_pendientes.filter(propiedad__ciudad__icontains=ciudad)
    if tipo_falla_id:
        pqr_pendientes = pqr_pendientes.filter(tipo_falla__id=tipo_falla_id)

    # --- Tipos de falla para el select ---
    tipos_falla = TipoFalla.objects.all()

    contexto = {
        "pendientes": pendientes,
        "en_curso": en_curso,
        "resueltos": resueltos,
        "estadisticas_ciudad": estadisticas_ciudad,
        "pqr_pendientes": pqr_pendientes,
        "tipos_falla": tipos_falla,
        "ciudad": ciudad,
        "tipo_falla_id": tipo_falla_id,
    }
    return render(request, 'reportes/dashboard.html', contexto)
