# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from ..registros.models import Oficina, Carrera, Perfil
from ..modulos.validators import valid_extension
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Entidad(Oficina):
    encargado = models.CharField(_('Responsable'), max_length=100)
    cargo = models.CharField(_('Cargo'), max_length=100)
    descripcion = models.TextField(_('Descripción'))
    carreras = models.ManyToManyField(Carrera, related_name='entidades')
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        permissions = [
            ('view_entidad', 'Puede acceder a Entidad'),
        ]

    def __unicode__(self):
        from django.utils.timezone import localtime, now

        if localtime(now()).date() > self.fin:
            return '{0} (Caduco)'.format(self.nombre, (self.fin-localtime(now()).date()).days)
        else:
            return '{0} (Restante: {1} dias)'.format(self.nombre, (self.fin-localtime(now()).date()).days)

def generate_evidencia_entidad(instance, filename):
    return 'entidad/{0}/{1}'.format(instance.entidad.nombre, filename)

class Evidencias_Entidad(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name='evidencias_entidad')
    imagen = models.ImageField(_(u'Evidencias Fotograficas'), upload_to=generate_evidencia_entidad)

    def __unicode__(self):
        return '{}'.format(self.entidad.nombre)

class Informe_vinculacion(models.Model):
    convenio = models.FileField(_('Convenio'), upload_to='informes_vinculacion', validators=[valid_extension])

    class Meta:
        permissions = [
            ('view_informe_vinculacion', 'Puede acceder a Informe Vinculacion'),
            ('reporte_convenio_vinculacion', 'Puede realizar el reporte de convenio'),
        ]

    def __unicode__(self):
        return '{}'.format(self.convenio)

###### Registro

class Actividad_vinculacion(models.Model):
    nombre = models.CharField(_(u'Nombre del Proyecto'), unique=True, max_length=150)
    inicio = models.DateField(auto_now_add=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='actividades_vinculacion')
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name='actividades_vinculacion')
    slug = models.SlugField(max_length=50, blank=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actividades_vinculacion')

    class Meta:
        permissions = [
            ('view_actividad_vinculacion', 'Puede acceder a Actividades de vinculacion'),
        ]

    def __unicode__(self):
        return '{}'.format(self.nombre)

########## Proyecto de Vinculacion
class Proyecto_vinculacion(models.Model):
    nombre = models.TextField(_(u'Nombre del Proyecto'))
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name='proyectos_vinculacion')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='proyectos_vinculacion')
    estado = models.BooleanField(default=True)
    inicio = models.DateField(auto_now_add=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proyectos_vinculacion')

    class Meta:
        permissions = [
            ('view_proyecto_vinculacion', 'Puede acceder a Registro Vinculacion'),
        ]

    def __unicode__(self):
        return '{}'.format(self.nombre)

class Componente(models.Model):
    proyecto_vinculacion = models.ForeignKey(Proyecto_vinculacion, on_delete=models.CASCADE, related_name='componentes')
    nombre = models.TextField(_('Nombre del Componente'))
    introduccion = models.TextField(_('Introduccion'), blank=True, null=True)
    observacion = models.TextField(_('Observaciones'), blank=True, null=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='componentes', blank=True, null=True)
    estado = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)], default=2)
    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        return '{}'.format(self.nombre)

class Objetivo(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='objectivos')
    nombre = models.TextField(_('Nombre del Componente'))

class Actividad(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='actividades')
    nombre = models.TextField(_('Nombre de la Actividad'))

class Proceso_actividad(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='proceso_actividades')
    realizado = models.TextField(_('Realizado'))
    meta = models.TextField(_('Meta'))
    resultado = models.TextField(_('Resultado'))
    cumplimiento = models.PositiveSmallIntegerField(_('% de Cumplimiento'), validators=[MinValueValidator(0), MaxValueValidator(100)])

class Recurso(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='recursos')
    nombre = models.CharField(_('Nombre del Recurso'), max_length=50)

class Proceso_recurso(models.Model):
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, related_name='proceso_recursos')
    nombre = models.TextField(_('Nombre de la Actividad'))

def generate_evidencia_proyecto(instance, filename):
    return 'proyectos/{0}/{1}/{2}'.format(instance.componente.proyecto_vinculacion.nombre, instance.componente.nombre, filename)

class Evidencia_proyecto(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='evidencias_proyecto')
    imagen = models.ImageField(upload_to=generate_evidencia_proyecto)

###### / Proyecto vinculacion