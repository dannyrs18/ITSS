from django.conf.urls import url
from . import views

app_name='practicas'
# Crear
urlpatterns = [
    url(r'^crear/$', views.crear, name='crear'),
    url(r'^crear_convenio/$', views.crear_convenio, name='crear_convenio'),
    url(r'^crear_empresa/$', views.crear_empresa, name='crear_empresa'),
]

# Actualizar
urlpatterns += [
    url(r'^proceso/(?P<slug>[-\w]+)/$', views.proceso, name='proceso'),
    url(r'^proceso_empresa/(?P<slug>[-\w]+)/$', views.proceso_empresa, name='proceso_empresa'),
    url(r'^actualizar_empresa/(?P<slug>[-\w]+)/$', views.actualizar_empresa, name='actualizar_empresa'),
]

# Tablas
urlpatterns += [
    url(r'^tabla/$', views.tabla, name='tabla'),
    url(r'^tabla_empresa_proceso/$', views.tabla_empresa_proceso, name='tabla_empresa_proceso'),
    url(r'^tabla_empresa/$', views.tabla_empresa, name='tabla_empresa'),
]

# Otros
urlpatterns += [
    url(r'^reporte_convenio/(?P<slug>[-\w]+)/$', views.reporte_convenio, name='reporte_convenio'),
    url(r'^reporte_estudiante/$', views.reporte_estudiante, name='reporte_estudiante'),
    url(r'^reporte_empresas/$', views.reporte_empresas, name='reporte_empresas'),
    url(r'^reporte_periodo/$', views.reporte_periodo, name='reporte_periodo'),
    url(r'^evidencia_empresa/$', views.evidencia_empresa, name='evidencia_empresa'),
    url(r'^evidencia_practicas/$', views.evidencia_practicas, name='evidencia_practicas'),
]