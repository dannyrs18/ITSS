# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from ..registros.models import Oficina, Carrera, Perfil, Estudiante
from ..modulos.validators import valid_extension

class Empresa(Oficina): # PRACTICAS
    gerente = models.CharField(_(u'Nombre del Gerente'), max_length=100)
    descripcion = models.TextField(_(u'Descripción'))
    carreras = models.ManyToManyField(Carrera, related_name='empresas')
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='empresas')

    class Meta:
        permissions = [
            ('view_empresa', 'Puede acceder a Empresa'),
            ('reporte_empresa', 'Puede acceder a reporte de Empresa')
        ]

    def __unicode__(self):
        from django.utils.timezone import localtime, now
        return '{0} (Restante: {1} dias)'.format(self.nombre, (self.fin-localtime(now()).date()).days)

def generate_evidencia_empresa(instance, filename):
    return 'empresas/{0}/{1}'.format(instance.empresa.nombre, filename)

class Evidencias_Empresa(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='evidencias_empresa')
    imagen = models.ImageField(_(u'Evidencias Fotograficas'), upload_to=generate_evidencia_empresa)

    def __unicode__(self):
        return '{}'.format(self.empresa.nombre)

class Informe_practicas(models.Model):
    convenio = models.FileField(upload_to='informes_practicas', validators=[valid_extension])

    class Meta:
        permissions = [
            ('view_informe_practicas', 'Puede acceder a Informe Practicas'),
            ('reporte_convenio_practicas', 'Puede realizar el reporte de convenio')
        ]

    def __unicode__(self):
        return '{}'.format(self.convenio)

class Registro_practicas(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='registros_practicas')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='registros_practicas') 
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='registros_practicas') 
    presentacion = models.DateField(_('Fecha de Presentacion')) #
    fin = models.DateField(_(u'Fecha de finalización'),blank=True, null=True)
    horas = models.PositiveIntegerField(_(u'Horas completadas'), default=0)
    calificacion = models.FloatField(_(u'Calificación del Estudiante'), default=0, validators=[MinValueValidator(0), MaxValueValidator(10)],)
    estado = models.BooleanField(_(u'Estado del registro'), default=True )# True si esta en proceso
    slug = models.SlugField(max_length=50, blank=True)

    class Meta:
        permissions = (
            ('view_registro_practicas', 'Puede visualizar el Registro'),
            ('reporte_registro_practicas', 'Puede acceder a reportes de Registro')
        )

    def __unicode__(self):
        return '{}'.format(self.estudiante)

def generate_registro_practicas(instance, filename):
    return 'registro_practicas/user_{0}/{1}'.format(instance.registro_practicas.estudiante.cedula, filename)

class Evidencias_registro_practicas(models.Model):
    registro_practicas = models.ForeignKey(Registro_practicas, on_delete=models.CASCADE, related_name='evidencias_registro_practicas')
    imagen = models.ImageField(_(u'Evidencias Fotograficas'), upload_to=generate_registro_practicas)

    def __unicode__(self):
        return '{}'.format(self.registro_practicas.estudiante.nombres+' '+self.registro_practicas.estudiante.apellidos)