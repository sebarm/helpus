from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
  path('', views.home, name="home"),
  path('nosotros', views.nosotros, name="nosotros"),
  path('registro', views.registro, name="registro"),
  path('login', views.login, name="login"),
  path('agregar_servicio', views.agregar_servicio, name="agregar_servicio"),
  path('listar_servicios', views.listar_servicios, name="listar_servicios"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)