from django.contrib.admin.widgets import AutocompleteSelect
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _



#usercreationform tiene un metodo para comparar las contraseñas automaticamente por eso no hay que hacerlo  
class CustomerUserCreationForm(UserCreationForm):
   
    def clean_fecha_nac(self):
        fecha_nac = self.cleaned_data.get('fecha_nac')
        if not fecha_nac:
            raise forms.ValidationError(_("La fecha de nacimiento es obligatoria"))
        return fecha_nac


    class Meta:
        model = User
        fields = '__all__'     

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