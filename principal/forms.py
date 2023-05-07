from django.contrib.admin.widgets import AutocompleteSelect
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _



#de esta forma transformo los campos en ingles del user default de django a español        
class CustomerUserCreationForm(UserCreationForm):
    tipo = forms.ModelChoiceField(queryset=TipoUsuario.objects.all(), label=_("Tipo de usuario"))
    nombre = forms.CharField(max_length=200, validators=[MinLengthValidator(2)], label=_("Nombre"))
    ap_paterno = forms.CharField(max_length=200, validators=[MinLengthValidator(2)], label=_("Apellido paterno"))
    ap_materno = forms.CharField(max_length=200, validators=[MinLengthValidator(2)], label=_("Apellido materno"))
    email = forms.EmailField( label=_("Correo electrónico"))
    contrasena = forms.CharField(max_length=10, widget=forms.PasswordInput, label=_("Contraseña"))
    direccion = forms.CharField(max_length=200, validators=[MinLengthValidator(5)], label=_("Dirección"))
    fecha_nac = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label=_("Fecha de nacimiento"),
        required=True,
)
    telefono = forms.CharField(max_length=200, validators=[RegexValidator(r'^\+?1?\d{9,15}$')], label=_("Teléfono"))
    puntuacion = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(7)], label=_("Puntuación"))
    
    
    def clean_fecha_nac(self):
        fecha_nac = self.cleaned_data.get('fecha_nac')
        if not fecha_nac:
            raise forms.ValidationError(_("La fecha de nacimiento es obligatoria"))
        return fecha_nac
    
    def __init__(self, *args, **kwargs):
        super(CustomerUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Usuario"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"