from django.conf.urls import url
from django.conf import settings
import views

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
    url(r'^reporte_estudiante/$', views.reporte_estudiante, name='reporte_estudiante'),
    url(r'^ajax_docente/$', views.ajax_docente, name='ajax_docente'),
    url(r'^ajax_estudiante/$', views.ajax_estudiante, name='ajax_estudiante'),
    url(r'^ajax_entidad/$', views.ajax_entidad, name='ajax_entidad'),
]

if settings.DEBUG: # Esto se ejecutara solamente cuando el modo desarrollo este activado ("DEBUG = TRUE" en el archivo settings) 
    urlpatterns += [
        url(r'^permisos/$', views.flush_permisos, name='permisos'),
    ]