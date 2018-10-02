from django.conf.urls import url
from . import views

app_name='vinculacion'
# Crear
urlpatterns = [
    url(r'^crear_proyecto/$', views.crear_proyecto, name='crear_proyecto'),
    url(r'^crear_componente/(?P<slug>[-\w]+)/$', views.crear_componente, name='crear_componente'),
    url(r'^crear_actividad/$', views.crear_actividad, name='crear_actividad'),
    url(r'^crear_convenio/$', views.crear_convenio, name='crear_convenio'),
    url(r'^crear_entidad/$', views.crear_entidad, name='crear_entidad'),
]

# Actualizar
urlpatterns += [
    url(r'^actualizar_entidad/(?P<slug>[-\w]+)/$', views.actualizar_entidad, name='actualizar_entidad'),
]

# Tablas
urlpatterns += [
    url(r'^tabla_proceso/$', views.tabla_proceso, name='tabla_proceso'),
    url(r'^tabla_entidad/$', views.tabla_entidad, name='tabla_entidad'),
]
# Otros
urlpatterns += [
    url(r'^reporte_convenio/(?P<slug>[-\w]+)/$', views.reporte_convenio, name='reporte_convenio'),
    url(r'^ajax_evidencia_entidad/$', views.ajax_evidencia_entidad, name='ajax_evidencia_entidad'),
]