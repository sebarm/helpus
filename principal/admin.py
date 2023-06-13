from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ServicioAdmin(admin.ModelAdmin):
    search_fields = ('nombre'),
    ordering = ['nombre'] 
    
class TipoUsuarioAdmin(admin.ModelAdmin):
    search_fields = ('nombre'),
    ordering = ['nombre']    
# Register your models here.
admin.site.register(Servicio, ServicioAdmin)  

class UserInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name = 'Usuarios'
    
class CustomizedUserAdmin (UserAdmin):
    inlines = (UserInline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
