from django.conf.urls import url
from . import views
from ..modulos.respaldo.views import dump_data, load_data

app_name='practicas'
# Crear
urlpatterns = [
    url(r'^crear/$', views.crear, name='crear'),
    url(r'^crear_convenio/$', views.crear_convenio, name='crear_convenio'),
    url(r'^crear_empresa/$', views.crear_empresa, name='crear_empresa'),
]

# Tablas
urlpatterns += [
    url(r'^tabla/$', views.tabla, name='tabla'),
    url(r'^tabla_empresa/$', views.tabla_empresa, name='tabla_empresa'),
]

urlpatterns += [
    url(r'^proceso/(?P<pk>\d+)/$', views.proceso, name='proceso'),
]

# Otros
urlpatterns += [
    url(r'^reporte_convenio/(?P<pk>\d+)/$', views.reporte_convenio, name='reporte_convenio'),
    url(r'^evidencia/$', views.evidencia, name='evidencia'),
]