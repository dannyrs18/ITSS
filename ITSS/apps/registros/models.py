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
    codigo = models.CharField(_(u'Codigo'), max_length=10)
    nombre = models.CharField(_(u'Nombre'), max_length=70)

    class Meta:
        permissions = [
            ('view_carrera', 'Puede acceder a Carrera'),
        ]

    def __unicode__(self):
        return self.nombre

class Estudiante(models.Model):
    nombres = models.CharField(_(u'Nombres'), max_length=50)
    apellidos = models.CharField(_(u'Apellidos'), max_length=50)
    cedula = models.CharField(_(u'Cedula'), max_length=30)
    genero = models.CharField(_(u'Genero'), max_length=30)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='estudiantes')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        permissions = (
            ('view_estudiante', 'Puede acceder a estudiante'),
            ('reporte_estudiante', 'Puede acceder a reportes de estudiante')
        )

    def __unicode__(self):
        return '{0} {1} - {2}'.format(self.nombres.partition(" ")[0], self.apellidos.partition(" ")[0], self.cedula)

    def get_full_name(self):
        return '{} {}'.format(self.nombres, self.apellidos)

class Docente(models.Model):
    nombres = models.CharField(_(u'Nombres'), max_length=50)
    apellidos = models.CharField(_(u'Apellidos'), max_length=50)
    telefono = models.CharField(_(u'Telefono'), max_length=15)
    cedula = models.CharField(_(u'Cedula'), max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('view_docente', 'Puede acceder a Docente'),
        ]

    def __unicode__(self):
        return '{0} {1} - {2}'.format(self.nombres.partition(" ")[0], self.apellidos.partition(" ")[0], self.cedula)

class Seccion(models.Model):
    identificador = models.CharField(max_length=4)
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return '{}'.format(self.identifiador)

class Oficina(models.Model): # Clase abstracta que usa practicas y vinculacion desde registros
    nombre = models.CharField(_(u'Nombre'), unique=True, max_length=100)
    logo = models.ImageField(_(u'Logo de la Empresa'), upload_to='logos', blank=True, null=True)
    telefono = models.CharField(_(u'Telefono'), max_length=15)
    inicio = models.DateField(_(u'Inicio del Convenio'))
    fin = models.DateField(_(u'Finalizacion del Convenio'))
    correo = models.EmailField(_(u'Correo'))
    direccion = models.TextField(_(u'Direccion'))
    estado = models.BooleanField(_(u'Estado'), default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, blank=True)

    class Meta:
        abstract = True

##### USUARIOS

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True, blank=True, related_name='perfiles')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=True, blank=True, related_name='perfiles')
    avatar = models.ImageField(_(u'Imagen de Perfil'), upload_to='img_perfil/', blank=True, null=True)
    slug = models.SlugField(max_length=50, blank=True)

    class Meta:
        permissions = (
            ("web_services", "Puede acceder a web_services"),
            ("view_reportes", "Puede acceder a reportes"),
            ("view_perfil", "Puede acceder a perfiles"),
            ("admin_vinc", "Administrador de Vinculacion"),
            ("admin_prac", "Administrador de Practicas"),
            ("resp_vinc",  "Responsable de Vinculacion"),
            ("resp_prac",  "Responsable de Practicas"),
        )

    def __unicode__(self):
        return self.user.username

    def get_simple_name(self):
        return '{0} {1}'.format(self.user.first_name.partition(" ")[0], self.user.last_name.partition(" ")[0])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()