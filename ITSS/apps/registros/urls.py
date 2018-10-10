from django.conf.urls import url
from django.conf import settings
import views

app_name='registro'
# Crear
urlpatterns = [
    url(r'^crear_usuario/$', views.crear_usuario, name='crear_usuario'),
    url(r'^crear_coordinador/$', views.crear_coordinador, name='crear_coordinador'),
]

# Modificar
urlpatterns += [
    url(r'^modificar_clave/$', views.modificar_clave, name='modificar_clave'),
    url(r'^modificar_estado/(?P<slug>[-\w]+)/$', views.modificar_estado, name='modificar_estado'),
    url(r'^modificar_usuario/(?P<pk>\d+)/$', views.modificar_usuario, name='modificar_usuario'),
]

# Tablas
urlpatterns += [
    url(r'^tabla_registros/$', views.tabla_registros, name='tabla_registros'),
    url(r'^tabla_usuarios/$', views.tabla_usuarios, name='tabla_usuarios'),
    url(r'^tabla_estudiantes/$', views.tabla_estudiantes, name='tabla_estudiantes'),
    url(r'^tabla_coordinadores/$', views.tabla_coordinadores, name='tabla_coordinadores'),
]

# Otros
urlpatterns += [
    url(r'^web_services/$', views.web_services, name='web_services'),
    url(r'^download_backup/$', views.download_backup, name='download_backup'),
    url(r'^create_backup/$', views.create_backup, name='create_backup'),
    url(r'^ajax_docente/$', views.ajax_docente, name='ajax_docente'),
    url(r'^ajax_estudiante/$', views.ajax_estudiante, name='ajax_estudiante'),
    url(r'^ajax_entidad/$', views.ajax_entidad, name='ajax_entidad'),
    url(r'^ajax_empresa_estudiante/$', views.ajax_empresa_estudiante, name='ajax_empresa_estudiante'),
    url(r'^ajax_entidad_estudiante/$', views.ajax_entidad_estudiante, name='ajax_entidad_estudiante'),
    url(r'^ajax_evidencia_estudiante/$', views.ajax_evidencia_estudiante, name='ajax_evidencia_estudiante'),
    url(r'^error/$', views.error, name='error'),
]

if settings.DEBUG: # Esto se ejecutara solamente cuando el modo desarrollo este activado ("DEBUG = TRUE" en el archivo settings) 
    urlpatterns += [
        url(r'^permisos/$', views.flush_permisos, name='permisos'),
    ]