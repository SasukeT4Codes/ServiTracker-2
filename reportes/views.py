from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pqr.models import PQR

# 📊 Dashboard principal (solo administradores y agentes)
@login_required
def dashboard(request):
    # Solo agentes y administradores
    if request.user.rol not in ["agente", "administrador"]:
        return redirect('index')

    # Contadores por estado
    pendientes = PQR.objects.filter(estado__nombre="Pendiente").count()
    en_curso = PQR.objects.filter(estado__nombre="En curso").count()
    resueltos = PQR.objects.filter(estado__nombre="Resuelto").count()

    # Estadísticas por ciudad
    estadisticas_ciudad = {}
    for pqr in PQR.objects.select_related('propiedad').all():
        if pqr.propiedad:
            ciudad = pqr.propiedad.ciudad
            if ciudad not in estadisticas_ciudad:
                estadisticas_ciudad[ciudad] = {"pendientes": 0, "resueltos": 0}
            if pqr.estado.nombre == "Pendiente":
                estadisticas_ciudad[ciudad]["pendientes"] += 1
            elif pqr.estado.nombre == "Resuelto":
                estadisticas_ciudad[ciudad]["resueltos"] += 1

    # Listado de PQR pendientes
    pqr_pendientes = PQR.objects.filter(estado__nombre="Pendiente")

    contexto = {
        "pendientes": pendientes,
        "en_curso": en_curso,
        "resueltos": resueltos,
        "estadisticas_ciudad": estadisticas_ciudad,
        "pqr_pendientes": pqr_pendientes,
    }
    return render(request, 'reportes/dashboard.html', contexto)
