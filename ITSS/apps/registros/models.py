# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

##### CARRERAS

class Carrera(models.Model):
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=70)

    def __unicode__(self):
        return self.nombre

##### USUARIOS

def generate_path(instance, filename):
    return os.path.join("id_" + str(instance.user.username), filename)

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(_('Imagen de Perfil'), upload_to=generate_path, blank=True, null=True)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    cedula = models.CharField(_('Cedula'), max_length=15)

    def __unicode__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()

#### BASE

class Estudiante(models.Model):
    nombres = models.CharField(_('Nombres'), max_length=50)
    apellidos = models.CharField(_('Apellidos'), max_length=50)
    cedula = models.CharField(_('Cedula'), max_length=30)
    genero = models.CharField(_('Genero'), max_length=30)
    #paralelo = models.ForeignKey(Paralelo, on_delete=models.CASCADE, related_name='estudiantes')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='estudiantes')
    #seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='estudiantes')
    #ciclo = models.CharField(max_length=50)
    #Periodo = models.CharField(max_length=50)

    def __unicode__(self):
        return '{0} {1}'.format(self.nombres, self.apellidos)

class Docentes(models.Model):
    nombres = models.CharField(_('Nombres'), max_length=50)
    apellidos = models.CharField(_('Apellidos'), max_length=50)
    telefono = models.CharField(_('Telefono'), max_length=15)
    cedula = models.CharField(_('Cedula'), max_length=15)

    def __unicode__(self):
        return '{0} {1}'.format(self.nombres, self.apellidos)

class Oficina(models.Model):
    nombre = models.CharField(_('Nombre'), max_length=100, unique=True)
    logo = models.ImageField(_('Logo'), upload_to='logos')
    telefono = models.CharField(_('Telefono'), max_length=15)
    inicio = models.DateField(_('Inicio'), blank=True, null=True)
    fin = models.DateField(_('Fin'), blank=True, null=True)
    correo = models.EmailField(_('Correo'), blank=True, null=True)
    direccion = models.TextField(_('Direccion'))
    estado = models.BooleanField(_('Estado'), default=False)
    coordinador = models.CharField(_('Coordinador'), max_length=50)

    class Meta:
        abstract = True