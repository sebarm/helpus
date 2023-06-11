from django.contrib.admin.widgets import AutocompleteSelect
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _



#usercreationform tiene un metodo para comparar las contraseñas automaticamente por eso no hay que hacerlo  
class CustomerUserCreationForm(UserCreationForm):
    tipo = forms.ModelChoiceField(queryset=TipoUsuario.objects.all(), label=_("Tipo de usuario"))
    nombre = forms.CharField(max_length=200, validators=[MinLengthValidator(2)], label=_("Nombre"))
    ap_paterno = forms.CharField(max_length=200, validators=[MinLengthValidator(2)], label=_("Apellido paterno"))
    ap_materno = forms.CharField(max_length=200, validators=[MinLengthValidator(2)], label=_("Apellido materno"))
    email = forms.EmailField(label=_("Correo electrónico"))
    direccion = forms.CharField(max_length=200, validators=[MinLengthValidator(5)], label=_("Dirección"))
    fecha_nac = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label=_("Fecha de nacimiento"),
        required=True,
    )
    telefono = forms.CharField(max_length=200, validators=[RegexValidator(r'^\+?1?\d{9,15}$')], label=_("Teléfono"))
    puntuacion = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(7)], label=_("Puntuación"))
    username = forms.CharField(max_length=200, validators=[MinLengthValidator(2)], label=_("Nombre de usuario"))

    def clean_fecha_nac(self):
        fecha_nac = self.cleaned_data.get('fecha_nac')
        if not fecha_nac:
            raise forms.ValidationError(_("La fecha de nacimiento es obligatoria"))
        return fecha_nac


    class Meta:
        model = User
        fields = ( 'username','tipo', 'nombre', 'ap_paterno','ap_materno','email', 'direccion', 'fecha_nac', 'telefono', 'puntuacion', 'password1', 'password2')        

class ServicioForm(forms.ModelForm):
    fecha_inicio = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label=_("Fecha de inicio"),
        required=True,
    )
    fecha_termino = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label=_("Fecha de termino"),
        required=True,
    )
    
    class Meta:
        model = Servicio
        fields = '__all__'        