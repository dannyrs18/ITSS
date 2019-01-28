#!/bin/bash

NAME="ITSS" # Nombre dela aplicación
DJANGODIR=/home/serveradmin/PracticasAcademicas/ITSS # Ruta dela carpeta donde esta la aplicación reemplazar <user> con el nombre de usuario
#SOCKFILE=/home/serveradmin/PracticasAcademicas/run/gunicorn.sock # Ruta donde se creará el archivo de socket unix para comunicarnos
DIRECCION=practicasacademicas.itss.edu.ec:80
USER=root # Usuario con el que vamos a correr laapp
GROUP=root # Grupo con el quese va a correr laapp
NUM_WORKERS=3 # Número de workers quese van a utilizar para correr la aplicación
DJANGO_SETTINGS_MODULE=proyecto.settings # ruta de los settings
DJANGO_WSGI_MODULE=proyecto.wsgi # Nombre del módulo wsgi

echo "Starting $NAME as `whoami`"

# Activar el entorno virtual
cd $DJANGODIR
source ../env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Crear la carpeta run si no existe para guardar el socket linux
# RUNDIR=$(dirname $SOCKFILE)
# test -d$RUNDIR || mkdir -p $RUNDIR

# Iniciar la aplicación django por medio de gunicorn
exec ../env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=$DIRECCION \
  --log-level=debug \
  --log-file=-

# invalid line: --user=$USER --group=$GROUP \
