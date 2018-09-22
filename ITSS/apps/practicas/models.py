# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from ..registros.models import Oficina, Carrera, Perfil, Estudiante
from ..modulos.validators import valid_extension

class Empresa(Oficina): # PRACTICAS
    gerente = models.CharField(_('Nombre del Gerente'), max_length=100)
    descripcion = models.TextField(_('Descricion'))
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

class Informe_practicas(models.Model):
    convenio = models.FileField(upload_to='informes_practicas', validators=[valid_extension])

    class Meta:
        permissions = [
            ('view_informe_practicas', 'Puede acceder a Informe Practicas'),
            ('reporte_convenio', 'Puede realizar el reporte de convenio')
        ]

    def __unicode__(self):
        return '{}'.format(self.convenio)

def generate_path(instance, filename):
    return 'estudiantes/user_{0}/{1}'.format(instance.estudiante.cedula, filename)

class Registro_practicas(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='registros_practicas')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='registros_practicas') 
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='registros_practicas') 
    presentacion = models.DateField(_('Fecha de Presentacion')) #
    fin = models.DateField(_(u'Fecha de finalización'),blank=True, null=True)
    horas = models.PositiveIntegerField(_(u'Horas completadas'), blank=True, null=True, default=0)
    calificacion = models.FloatField(_(u'Calificación del Estudiante'), blank=True, null=True, default=0)
    solicitud = models.ImageField(_(u'Evidencia de Solicitud'), upload_to=generate_path)
    aceptacion = models.ImageField(_(u'Evidencia de Aceptación'), upload_to=generate_path)
    evaluacion = models.ImageField(_(u'Evidencia de Evaluación'), upload_to=generate_path, blank=True, null=True)
    culminacion = models.ImageField(_(u'Evidencia de Culminación'), upload_to=generate_path, blank=True, null=True)
    estado = models.BooleanField(_(u'Estado del registro'), default=True )# True si esta en proceso

    class Meta:
        permissions = (
            ('view_registro_practicas', 'Puede visualizar el Registro'),
            ('reporte_registro_practicas', 'Puede acceder a reportes de Registro')
        )

    def __unicode__(self):
        return '{}'.format(self.estudiante)