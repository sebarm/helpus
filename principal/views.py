from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    servicios = Servicio.objects.all()
    
    data = {
        'servicios' : servicios
    }
    
    return render(request, 'front/home.html',data)

def nosotros(request):
    return render(request, 'front/nosotros.html')

def recovery(request):
    return render(request, 'registration/recovery.html')


def changePassword(request):
    return render(request, 'registration/changePassword.html')


def registro(request):

    data = {
        'form': CustomerUserCreationForm()
    }
    
    if request.method == 'POST':
        formulario =CustomerUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            Usuario.objects.create(user=user, nombre=user.username, email= formulario.cleaned_data["email"], fecha_nac= formulario.cleaned_data["fecha_nac"], telefono= formulario.cleaned_data["telefono"], direccion= formulario.cleaned_data["direccion"], tipo= formulario.cleaned_data["tipo"], puntuacion= formulario.cleaned_data["puntuacion"], ap_paterno= formulario.cleaned_data["ap_paterno"], ap_materno= formulario.cleaned_data["ap_materno"]         )
            login(request, user)
            messages.success(request, "Registro con éxito ahora puedes solicitar o tambien ofrecer servicios")
            return redirect(to="home")
        data["form"] = formulario
    
    
    return render(request, 'registration/registro.html',data)

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
        servicio.usuario_realizador = None
        servicio.save()
        messages.success(request, "Servicio liberado correctamente.")
    else:
        messages.error(request, "No tienes permiso para liberar este servicio.")

    return redirect('home')