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
  path('recovery', views.recovery, name="recovery"),
  path('changePassword', views.changePassword, name="changePassword"),
  path('guardar_servicio/', views.guardar_servicio, name='guardar_servicio'),
  path('eliminar_servicio/<int:servicio_id>/', views.eliminar_servicio, name='eliminar_servicio'),
  path('liberar_servicio/<int:servicio_id>/', views.liberar_servicio, name='liberar_servicio'),
  path('perfil/p.usuario_creador.id', views.perfil, name='perfil'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)