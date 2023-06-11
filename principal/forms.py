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

    def save(self, commit=True):
        user = super(CustomerUserCreationForm, self).save(commit=False)
        if commit:
            user.save()
            user.nombre = self.cleaned_data["nombre"]
            user.ap_paterno = self.cleaned_data["ap_paterno"]
            user.ap_materno = self.cleaned_data["ap_materno"]
            user.email = self.cleaned_data["email"]
            user.direccion = self.cleaned_data["direccion"]
            user.fecha_nac = self.cleaned_data["fecha_nac"]
            user.telefono = self.cleaned_data["telefono"]
            user.tipo = self.cleaned_data["tipo"]
            user.puntuacion = self.cleaned_data["puntuacion"]
            user.save()
        return user

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