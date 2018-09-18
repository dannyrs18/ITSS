# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models

#def generate_path(instance, filename):
#    return 'estudiantes/user_{0}/{1}'.format(instance.estudiante.cedula, filename)
#(upload_to=generate_path)

##### REGISTROS

class Carrera(models.Model):
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=70)

    def __unicode__(self):
        return self.nombre

class Estudiante(models.Model):
    nombres = models.CharField(_('Nombres'), max_length=50)
    apellidos = models.CharField(_('Apellidos'), max_length=50)
    cedula = models.CharField(_('Cedula'), max_length=30)
    genero = models.CharField(_('Genero'), max_length=30)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='estudiantes')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        permissions = (
            ('view_estudiante', 'Puede acceder a estudiante'),
        )

    def __unicode__(self):
        return '{0} {1} - {2}'.format(self.nombres.partition(" ")[0], self.apellidos.partition(" ")[0], self.cedula)

class Docente(models.Model):
    nombres = models.CharField(_('Nombres'), max_length=50)
    apellidos = models.CharField(_('Apellidos'), max_length=50)
    telefono = models.CharField(_('Telefono'), max_length=15)
    cedula = models.CharField(_('Cedula'), max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0} {1} - {2}'.format(self.nombres.partition(" ")[0], self.apellidos.partition(" ")[0], self.cedula)

class Oficina(models.Model): # Clase abstracta que usa practicas y vinculacion desde registros
    nombre = models.CharField(_('Nombre'), max_length=100, unique=True)
    logo = models.ImageField(_('Logo'), upload_to='logos', blank=True, null=True)
    telefono = models.CharField(_('Telefono'), max_length=15)
    inicio = models.DateField(_('Inicio del Convenio'))
    fin = models.DateField(_('Finalizacion del Convenio'))
    correo = models.EmailField(_('Correo'))
    direccion = models.TextField(_('Direccion'))
    estado = models.BooleanField(_('Estado'), default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

##### USUARIOS

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True, blank=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(_('Imagen de Perfil'), upload_to='img_perfil/', blank=True, null=True)

    class Meta:
        permissions = (
            ("admin_vinc", "Administrador de Vinculacion"),
            ("admin_prac", "Administrador de Practicas"),
            ("resp_vinc",  "Responsable de Vinculacion"),
            ("resp_prac",  "Responsable de Practicas"),
        )

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()