from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from pqr.models import PQR, TipoFalla

# 📊 Dashboard del administrador
@user_passes_test(lambda u: u.is_staff or u.rol == "administrador")
def dashboard_admin(request):
    ciudad = request.GET.get("ciudad")
    tipo_falla_id = request.GET.get("tipo_falla")

    pendientes = PQR.objects.filter(estado__nombre="Pendiente").count()
    en_curso = PQR.objects.filter(estado__nombre="En curso").count()
    resueltos = PQR.objects.filter(estado__nombre="Resuelto").count()

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

    pqr_pendientes = PQR.objects.filter(estado__nombre="Pendiente")
    if ciudad:
        pqr_pendientes = pqr_pendientes.filter(propiedad__ciudad__icontains=ciudad)
    if tipo_falla_id:
        pqr_pendientes = pqr_pendientes.filter(tipo_falla__id=tipo_falla_id)

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
    return render(request, 'reportes/dashboard_admin.html', contexto)


# 📊 Dashboard del agente
@user_passes_test(lambda u: u.rol == "agente")
def dashboard_agente(request):
    ciudad = request.GET.get("ciudad")
    tipo_falla_id = request.GET.get("tipo_falla")

    pendientes = PQR.objects.filter(estado__nombre="Pendiente").count()
    en_curso = PQR.objects.filter(estado__nombre="En curso").count()
    resueltos = PQR.objects.filter(estado__nombre="Resuelto").count()

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

    pqr_pendientes = PQR.objects.filter(estado__nombre="Pendiente")
    if ciudad:
        pqr_pendientes = pqr_pendientes.filter(propiedad__ciudad__icontains=ciudad)
    if tipo_falla_id:
        pqr_pendientes = pqr_pendientes.filter(tipo_falla__id=tipo_falla_id)

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
    return render(request, 'reportes/dashboard_agente.html', contexto)


# 📊 Dashboard del técnico
@user_passes_test(lambda u: u.rol == "tecnico")
def dashboard_tecnico(request):
    pqr_asignadas = PQR.objects.filter(tecnico=request.user)
    return render(request, "reportes/dashboard_tecnico.html", {
        "usuario": request.user,
        "pqr_asignadas": pqr_asignadas,
    })
