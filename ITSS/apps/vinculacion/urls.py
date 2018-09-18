from django.conf.urls import url
from . import views
from ..modulos.respaldo.views import dump_data, load_data

app_name='vinculacion'
# Crear
urlpatterns = [
    url(r'^crear_convenio/$', views.crear_convenio, name='crear_convenio'),
    url(r'^crear_entidad/$', views.crear_entidad, name='crear_entidad'),
]
# Otros
urlpatterns += [
    url(r'^evidencia/$', views.evidencia, name='evidencia'),
]