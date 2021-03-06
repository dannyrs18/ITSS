"""
Django settings for proyecto project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def path(dir):
    return os.path.join(BASE_DIR, dir)
    
# def enc(key):
#     password = ''
#     for caracter in key:
#         password = password + chr(ord(caracter) - 3)
#     return password



SECRET_KEY = 'y$xt2htr-dkxx8*&q65a!^$ej*kff^a6(tm9lcldbp%qr-nfk('

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'dbbackup',
    'apps.registros',
    'apps.practicas',
    'apps.vinculacion',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proyecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path('templates/templates'),
            path('templates/pages'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'proyecto.wsgi.application'

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'academico',
        'USER': 'practicas',
        'PASSWORD': 'tesis',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
        },
    }, # LA BASE DE DATOS TIENE PRIVILEGIOS LIMITADOS
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-ec'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Archivos estaticos
STATIC_URL = '/static/' # RUTA DE URL PARA LOS STATICFILES (localhost/static/....)
STATICFILES_DIRS = [ 
    path('desarrollo/assets')
]# si los estatics no se encuentran dentro de las aplicacion donde por default se buscan los archivos, aqui se especifican las carpetas adicionales
STATIC_ROOT = path('static')

# Archivos medios
MEDIA_URL = '/media/'
MEDIA_ROOT = path('media')

# Redirecciona cuando se inicia sesion 
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('login')
LOGIN_URL = reverse_lazy('login')

# Formato de Fecha
DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')

# Servidor de correos
EMAIL = 'practicas.vinculacionitss@gmail.com'
# variable para reusar
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_HOST_USER =  EMAIL# Gmail del emisor del mensaje
EMAIL_HOST_PASSWORD = 'practicas'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SEND_EMAIL=True # Estado para activar los correos

# Respaldo
PATH_BACKUP = path('backups') # Direccion donde se guardara los respaldos
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_CLEANUP_KEEP = 5
DBBACKUP_CLEANUP_KEEP_MEDIA = 5
DBBACKUP_STORAGE_OPTIONS = {'location': PATH_BACKUP}

# Cron
PATH_CRON = path('desarrollo/cron.log') # Direccion donde se guardara informacion de acctualizaciones
CRONJOBS  = [
    # 
    ('@daily' , 'apps.registros.views.update', '>> '+PATH_CRON), # Actualizacion diariamente
    ('* * * 5 *' , 'django.core.management.call_command', ['dbbackup']), # Actualizacion cada 5 meses
    ('* * * 5 *' , 'django.core.management.call_command', ['mediabackup']), # Actualizacion cada 5 meses
]
