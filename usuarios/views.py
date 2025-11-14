from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegistroForm, LoginForm
from django.contrib.auth import get_user_model

Usuario = get_user_model()

# 🌐 Vista principal del sitio (landing page)
def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {
            'usuario': request.user,
            'rol': request.user.rol
        })
    return render(request, 'index.html')

# 📝 Vista para registrar un nuevo usuario (público)
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

# 🔐 Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

# 🚪 Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('index')

# 👤 Vista del perfil del usuario
@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})

# 📋 Vista para listar usuarios (solo admin/staff)
@user_passes_test(lambda u: u.is_staff or u.rol == "administrador")
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

# ➕ Vista para crear usuarios (solo admin/staff)
@user_passes_test(lambda u: u.is_staff or u.rol == "administrador")
def crear_usuario(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_usuarios")
    else:
        form = RegistroForm()
    return render(request, "usuarios/crear_usuario.html", {"form": form})
