from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm

# 🌐 Vista principal del sitio (landing page)
def index(request):
    if request.user.is_authenticated:
        # Pasamos el rol y el usuario al template
        return render(request, 'index.html', {
            'usuario': request.user,
            'rol': request.user.rol
        })
    return render(request, 'index.html')

# 📝 Vista para registrar un nuevo usuario
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()         # guarda el nuevo usuario
            login(request, usuario)       # inicia sesión automáticamente
            return redirect('index')      # redirige al inicio
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

# 🔐 Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()     # obtiene el usuario autenticado
            login(request, usuario)       # inicia sesión
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

# 🚪 Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('index')

# 👤 Vista del perfil del usuario (solo si está logueado)
@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})
