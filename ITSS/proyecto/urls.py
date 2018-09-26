from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^registro/', include('apps.registros.urls')),
    url(r'^practicas/', include('apps.practicas.urls')),
    url(r'^vinculacion/', include('apps.vinculacion.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]
if settings.DEBUG: # Esto se ejecutara solamente cuando el modo desarrollo este activado ("DEBUG = TRUE" en el archivo settings) 
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), # la vista serve es un paquete estatico de django que se encarga de servir directorios, el parametro que debemos asignarle es la ruta en 'document_root'(normalmente llamamos a MEDIA_ROOT que es la que sirve los archivos media) /recomendan usar servidores dedicados/
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)