from django.conf.urls import url
from . import views

app_name='registro'
# Crear
urlpatterns = [
    url(r'^crear_usuario/$', views.crear_usuario, name='crear_usuario'),
]