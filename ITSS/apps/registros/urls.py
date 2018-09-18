from django.conf.urls import url
from . import views
from ..modulos.respaldo.views import dump_data, load_data

app_name='registro'
# Crear
urlpatterns = [
    url(r'^crear_usuario/$', views.crear_usuario, name='crear_usuario'),
]

# Tablas
urlpatterns += [
    url(r'^tabla_registros/$', views.tabla_registros, name='tabla_registros'),
    url(r'^tabla_estudiantes/$', views.tabla_estudiantes, name='tabla_estudiantes'),
]

# Otros
urlpatterns += [
    url(r'^web_services/$', views.web_services, name='web_services'),
    url(r'^ajax_docente/$', views.ajax_docente, name='ajax_docente'),
    url(r'^ajax_estudiante/$', views.ajax_estudiante, name='ajax_estudiante'),
    url(r'^dump/$', dump_data, name='dump-data'),
    url(r'^load/$', load_data, name='load-data'),
]