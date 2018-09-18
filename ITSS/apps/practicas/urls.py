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

urlpatterns += [
    url(r'^tabla/$', views.tabla, name='tabla'),
]

# Otros
urlpatterns += [
    url(r'^evidencia/$', views.evidencia, name='evidencia'),
]