from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import timezone
# Create your views here.
def home(request):
    servicios = Servicio.objects.all()
    usuarios = Usuario.objects.all()
    data = {
        'servicios' : servicios,
        'usuarios' : usuarios,
        
    }
    
    return render(request, 'front/home.html',data)

def nosotros(request):
    return render(request, 'front/nosotros.html')

def recovery(request):
    return render(request, 'registration/recovery.html')


def changePassword(request):
    return render(request, 'registration/changePassword.html')

@login_required
def perfil(request, id):
    user = request.user
    usuario = request.user.usuario  # Modifica esta línea
    servicios_aceptados = usuario.servicios_aceptados()
    perfil = get_object_or_404(Usuario, id = id)
    
    usuariosRegistrado = Usuario.objects.all()
    data = {
        'user' : user,
        'usuario' : usuario,
        'usuarios_registrado': usuariosRegistrado,
        'servicios_aceptados': servicios_aceptados,
        'perfil': perfil
        
    }
    
    # Otros códigos relacionados con el perfil
    return render(request, 'front/perfil.html', data)




def registro(request):
    form = CustomerUserCreationForm()
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.usuario = Usuario.objects.create(
                user=user,
                nombre=form.cleaned_data["nombre"],
                ap_paterno=form.cleaned_data["ap_paterno"],
                ap_materno=form.cleaned_data["ap_materno"],
                email=form.cleaned_data["email"],
                direccion=form.cleaned_data["direccion"],
                fecha_nac=form.cleaned_data["fecha_nac"],
                telefono=form.cleaned_data["telefono"],
                tipo=form.cleaned_data["tipo"],
                puntuacion=form.cleaned_data["puntuacion"]
            )
            user.save()
            login(request, user)
            messages.success(request, "Registro exitoso, ahora puedes solicitar o también ofrecer servicios.")
            return redirect('home')
    return render(request, 'registration/registro.html', {'form': form})
def agregar_servicio(request):

    data= {
            'servicio_form': ServicioForm()
        }    
   
    if request.method == 'POST':
            formulario = ServicioForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                formulario.save()
                messages.success(request, "Servicio creado con éxito")    
                data["mensaje"] = "guardado"
            else:
                data ["form"] = formulario
    return render(request, 'back/agregar_servicio.html', data);

@login_required
def listar_servicios(request):
    servicios = Servicio.objects.all()
    
    data = {
        'servicios': servicios
    }
    return render(request, 'back/listar_servicios.html', data)

@login_required
def guardar_servicio(request):
    if request.method == 'POST':
        servicio_id = request.POST.get('servicio_id')
        servicio = get_object_or_404(Servicio, id=servicio_id)
        request.user.servicio_asignado = servicio
        request.user.save()

        servicio.usuario_realizador = request.user
        servicio.save()

        messages.success(request, "Servicio asignado correctamente.")
        return redirect('home')
    else:
        return redirect('listar_servicios')

@login_required
def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        # Eliminar el servicio
        servicio.delete()
        messages.success(request, "Servicio eliminado correctamente.")
    else:
        messages.error(request, "Error al eliminar el servicio.")

    return redirect('home')

@login_required
def liberar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if servicio.usuario_realizador == request.user:
        fecha_termino = servicio.fecha_termino
        fecha_actual = timezone.now()

        if fecha_termino - timedelta(days=7) >= fecha_actual:
            servicio.usuario_realizador = None
            servicio.save()
            messages.success(request, "Servicio liberado correctamente.")
        else:
            messages.error(request, "No puedes liberar este servicio debido a conflictos con la fecha")
    else:
        messages.error(request, "No tienes permiso para liberar este servicio.")

    return redirect('home')