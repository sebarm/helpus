
from django.contrib.auth.models import User
import datetime
from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, EmailValidator,MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


def validar_fechas(fecha_inicio, fecha_termino):
    if fecha_inicio > fecha_termino:
        raise ValidationError('La fecha de inicio no puede ser posterior a la fecha de término.')
    if fecha_termino < fecha_inicio:
        raise ValidationError('La fecha de término no puede ser anterior a la fecha de inicio.')


class Servicio(models.Model):
    nombre = models.CharField(max_length=200, unique=True, validators=[MaxLengthValidator(200)])
    descripcion = models.CharField(max_length=200, validators=[MaxLengthValidator(200)])
    fecha_creacion = models.DateField(auto_now_add=True)
    estado_servicio = models.BooleanField(default=True)
    direccion = models.CharField(max_length=200, validators=[MaxLengthValidator(200)])
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_termino = models.DateTimeField(null=True, blank=True)
    usuario_realizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    usuario_creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios_creados')
    

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        db_table = 'Servicio'

    def clean(self):
        # Validación de fecha de creación
        

        # Validación de campo estado_servicio
        if self.estado_servicio not in [True, False]:
            raise ValidationError('El campo estado_servicio debe tener un valor booleano.')
        validar_fechas(self.fecha_inicio, self.fecha_termino)

class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500) 
    creado= models.DateTimeField(auto_now_add=True) 
    modificado= models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'TipoUsuario'
        verbose_name_plural = 'tipoUsuarios'
        db_table = 'tipoUsuarios'


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoUsuario,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    ap_paterno = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    ap_materno = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    email = models.EmailField()
    direccion = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    fecha_nac = models.DateTimeField()
  
    telefono = models.CharField(
        max_length=200,validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    puntuacion = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(7)])
    
    
    def servicios_aceptados(self):
        return Servicio.objects.filter(usuario_realizador=self.user)
    
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'Usuario'
        
        
    def calcular_edad(self):
        hoy = datetime.date.today()
        cumpleanios = self.fecha_nac
        edad = hoy.year - cumpleanios.year - ((hoy.month, hoy.day) < (cumpleanios.month, cumpleanios.day))
        return edad    
        
    
        # Validación de fecha de nacimiento
     
        
        # Validación de puntuación máxima
       


class ServicioOfrecido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_termino = models.DateField(null=True, blank=True)
    estado_servicio = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'ServicioOfrecido'
        verbose_name_plural = 'ServiciosOfrecidos'
        db_table = 'ServicioOfrecido'
        
        
    def clean(self):
        # Validación de fechas
        if self.fecha_inicio > self.fecha_termino:
            raise ValidationError('La fecha de inicio no puede ser posterior a la fecha de término.')
        if self.fecha_termino < self.fecha_inicio:
            raise ValidationError('La fecha de término no puede ser anterior a la fecha de inicio.')

        # Validación de campo estado_servicio
        if self.estado_servicio not in [True, False]:
            raise ValidationError('El campo estado_servicio debe tener un valor booleano.')   
        
        # Validación de solapamiento de fechas con otros servicios del usuario
        servicios_usuario = ServicioOfrecido.objects.filter(usuario=self.usuario).exclude(id=self.id)
        for servicio in servicios_usuario:
            if self.fecha_inicio <= servicio.fecha_termino and self.fecha_termino >= servicio.fecha_inicio:
                raise ValidationError('El servicio topa en horario con otro servicio del usuario.')
            validar_fechas(self.fecha_inicio, self.fecha_termino)
        # otros validaciones
            
            
class ServicioSolicitado(models.Model):   
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_termino = models.DateField(null=True, blank=True)
    estado_servicio = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'ServiciosSolicitado'
        verbose_name_plural = 'serviciosSolicitados'
        db_table = 'ServicioSolicitado'

        
    def clean(self):
        # Validación de fechas
        if self.fecha_inicio > self.fecha_termino:
            raise ValidationError('La fecha de inicio no puede ser posterior a la fecha de término.')
        if self.fecha_termino < self.fecha_inicio:
            raise ValidationError('La fecha de término no puede ser anterior a la fecha de inicio.')
        validar_fechas(self.fecha_inicio, self.fecha_termino)
        # otros validaciones

        # Validación de campo estado_servicio
        if self.estado_servicio not in [True, False]:
            raise ValidationError('El campo estado_servicio debe tener un valor booleano.')   
        
        # Validación de solapamiento de fechas con otros servicios del usuario
        servicios_usuario = ServicioSolicitado.objects.filter(usuario=self.usuario).exclude(id=self.id)
        for servicio in servicios_usuario:
            if self.fecha_inicio <= servicio.fecha_termino and self.fecha_termino >= servicio.fecha_inicio:
                raise ValidationError('El servicio se solapa con otro servicio del usuario.')
            
            

    
    
            
                       