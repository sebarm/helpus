from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    return render(request, 'front/home.html')

def nosotros(request):
    return render(request, 'front/nosotros.html')

def registro(request):

    data = {
        'form': CustomerUserCreationForm()
    }
    
    if request.method == 'POST':
        formulario =CustomerUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            Usuario.objects.create(user=user, nombre=user.username, email=user.email, fecha_nac= formulario.cleaned_data["fecha_nac"], telefono= formulario.cleaned_data["telefono"], direccion= formulario.cleaned_data["direccion"], tipo= formulario.cleaned_data["tipo"], puntuacion= formulario.cleaned_data["puntuacion"]         )
            login(request, user)
            messages.success(request, "Registro con éxito ahora puedes comprar en nuestra tienda")
            return redirect(to="home")
        data["form"] = formulario
    
    
    return render(request, 'registration/registro.html',data)