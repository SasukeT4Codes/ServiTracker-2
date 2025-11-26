from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from pqr.models import PQR, TipoFalla, Propiedad

# 📊 Dashboard del administrador
@user_passes_test(lambda u: u.is_staff or u.rol == "administrador")
def dashboard_admin(request):
    pendientes = PQR.objects.filter(estado__nombre="Pendiente").count()
    en_curso = PQR.objects.filter(estado__nombre="En curso").count()
    resueltos = PQR.objects.filter(estado__nombre="Resuelto").count()

    # Estadísticas por ciudad
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

    # Top 5 urgentes/muy urgentes, si no hay mostrar pendientes
    pqr_urgentes = PQR.objects.filter(estado__nombre__in=["Urgente", "Muy urgente"]).order_by("id")[:5]
    if not pqr_urgentes.exists():
        pqr_urgentes = PQR.objects.filter(estado__nombre="Pendiente").order_by("id")[:5]

    # Últimas 5 resueltas
    pqr_resueltas = PQR.objects.filter(estado__nombre="Resuelto").order_by("-id")[:5]

    contexto = {
        "pendientes": pendientes,
        "en_curso": en_curso,
        "resueltos": resueltos,
        "estadisticas_ciudad": estadisticas_ciudad,
        "pqr_urgentes": pqr_urgentes,
        "pqr_resueltas": pqr_resueltas,
    }
    return render(request, 'reportes/dashboard_admin.html', contexto)


# 📊 Dashboard del agente
@user_passes_test(lambda u: u.rol == "agente")
def dashboard_agente(request):
    # El agente gestiona PQR operativamente: ver pendientes y en curso
    pqr_pendientes = PQR.objects.filter(estado__nombre="Pendiente")
    pqr_en_curso = PQR.objects.filter(estado__nombre="En curso")

    ciudad = request.GET.get("ciudad")
    if ciudad:
        pqr_pendientes = pqr_pendientes.filter(propiedad__ciudad__icontains=ciudad)
        pqr_en_curso = pqr_en_curso.filter(propiedad__ciudad__icontains=ciudad)

    contexto = {
        "usuario": request.user,
        "pqr_pendientes": pqr_pendientes,
        "pqr_en_curso": pqr_en_curso,
        "ciudad": ciudad or "",
    }
    return render(request, 'reportes/dashboard_agente.html', contexto)


# 📊 Dashboard del técnico
@user_passes_test(lambda u: u.rol == "tecnico")
def dashboard_tecnico(request):
    pqr_asignadas = PQR.objects.filter(tecnico_asignado=request.user)
    return render(request, "reportes/dashboard_tecnico.html", {
        "usuario": request.user,
        "pqr_asignadas": pqr_asignadas,
    })


# 📋 Todas las PQR (con filtros)
@user_passes_test(lambda u: u.is_staff or u.rol == "administrador")
def lista_todas_pqr(request):
    ciudad = request.GET.get("ciudad", "")
    tipo_falla_id = request.GET.get("tipo_falla", "")

    pqr_list = PQR.objects.all()
    if ciudad:
        pqr_list = pqr_list.filter(propiedad__ciudad__icontains=ciudad)
    if tipo_falla_id:
        pqr_list = pqr_list.filter(tipo_falla_id=tipo_falla_id)

    tipos_falla = TipoFalla.objects.all()

    return render(request, "reportes/lista_todas.html", {
        "pqr_list": pqr_list,
        "ciudad": ciudad,
        "tipo_falla_id": tipo_falla_id,
        "tipos_falla": tipos_falla,
    })
