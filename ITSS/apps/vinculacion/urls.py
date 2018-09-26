from django.conf.urls import url
from . import views
from ..modulos.respaldo.views import dump_data, load_data

app_name='vinculacion'
# Crear
urlpatterns = [
    url(r'^crear_proyecto/$', views.crear_proyecto, name='crear_proyecto'),
    url(r'^crear_componente/(?P<slug>[-\w]+)/$', views.crear_componente, name='crear_componente'),
    url(r'^crear_actividad/$', views.crear_actividad, name='crear_actividad'),
    url(r'^crear_convenio/$', views.crear_convenio, name='crear_convenio'),
    url(r'^crear_entidad/$', views.crear_entidad, name='crear_entidad'),
]
# Tablas
urlpatterns += [
    url(r'^tabla_proceso/$', views.tabla_proceso, name='tabla_proceso'),
]
# Otros
urlpatterns += [
    url(r'^evidencia/$', views.evidencia, name='evidencia'),
]