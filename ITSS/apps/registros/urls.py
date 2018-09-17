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
    url(r'^registros/$', views.registros, name='registros'),
]

# Otros
urlpatterns += [
    url(r'^web_services/$', views.web_services, name='web_services'),
    url(r'^dump/$', dump_data, name='dump-data'),
    url(r'^load/$', load_data, name='load-data')
]