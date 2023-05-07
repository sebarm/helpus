from django.contrib import admin
from .models import *


class ServicioAdmin(admin.ModelAdmin):
    search_fields = ('nombre'),
    ordering = ['nombre'] 
    
class TipoUsuarioAdmin(admin.ModelAdmin):
    search_fields = ('nombre'),
    ordering = ['nombre']    
# Register your models here.
admin.site.register(Servicio, ServicioAdmin)  
admin.site.register(TipoUsuario, TipoUsuarioAdmin) 

