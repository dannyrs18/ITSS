# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from ..registros.models import Oficina, Carrera, Perfil, Estudiante, Seccion
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ..modulos.validators import valid_extension, valid_extension_docx

class Entidad(Oficina):
    encargado = models.CharField(_('Responsable'), max_length=100)
    cargo = models.CharField(_('Cargo'), max_length=100)
    fax = models.CharField(_('Fax'), max_length=20, blank=True, null=True)
    descripcion = models.TextField(_('Descripción'))
    carreras = models.ManyToManyField(Carrera, related_name='entidades')
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        permissions = [
            ('view_entidad', 'Puede acceder a Entidad'),
            ('reporte_entidad', 'Puede acceder a reporte de Entidad')
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
    convenio = models.FileField(_('Convenio'), upload_to='informes_vinculacion', validators=[valid_extension_docx])

    class Meta:
        permissions = [
            ('view_informe_vinculacion', 'Puede acceder a Informe Vinculacion'),
            ('reporte_convenio_vinculacion', 'Puede realizar el reporte de convenio'),
        ]

    def __unicode__(self):
        return '{}'.format(self.convenio)

###### Registro

class Actividad_vinculacion(models.Model):
    nombre = models.CharField(_(u'Nombre de la Actividad'), max_length=300)
    inicio = models.DateField(_(u'Fecha de inicio'))
    fin = models.DateField(_(u'Fecha de culminación'))
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='actividades_vinculacion')
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name='actividades_vinculacion')
    slug = models.SlugField(max_length=50, blank=True)
    descripcion = models.TextField(_(u'Descripción'))
    justificacion = models.TextField(_(u'Justificación'))
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actividades_vinculacion')

    class Meta:
        permissions = [
            ('view_actividad_vinculacion', 'Puede acceder a Actividades de vinculacion'),
        ]

    def __unicode__(self):
        return '{}'.format(self.nombre)

class Objetivo_Especifico(models.Model):
    actividad_vinculacion = models.ForeignKey(Actividad_vinculacion, on_delete=models.CASCADE, related_name='objetivos_especificos')
    nombre = models.TextField(_(u'Objetivos Especificos'))

    def __unicode__(self):
        return u'{}'.format(self.nombre)

class Objetivo_General(models.Model):
    actividad_vinculacion = models.ForeignKey(Actividad_vinculacion, on_delete=models.CASCADE, related_name='objetivos_generales')
    nombre = models.TextField(_(u'Objetivos Generales'))

    def __unicode__(self):
        return u'{}'.format(self.nombre)

class Actividad_Ac(models.Model):
    actividad_vinculacion = models.ForeignKey(Actividad_vinculacion, on_delete=models.CASCADE, related_name='actividades_ac')
    nombre = models.TextField(_(u'Actividades'))

    def __unicode__(self):
        return u'{}'.format(self.nombre)

def generate_evidencia_actividad(instance, filename):
    return 'actividades/{0}/{1}'.format(instance.actividad.nombre, filename)

class Evidencia_actividad(models.Model):
    actividad = models.ForeignKey(Actividad_vinculacion, on_delete=models.CASCADE, related_name='evidencias_actividades')
    imagen = models.ImageField(upload_to=generate_evidencia_actividad, max_length=200)

    def __unicode__(self):
        return '{}'.format(self.imagen.url)

########## Proyecto de Vinculacion
class Proyecto_vinculacion(models.Model):
    nombre = models.CharField(_(u'Nombre del Proyecto'), max_length=300)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name='proyectos_vinculacion')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='proyectos_vinculacion')
    estado = models.BooleanField(default=True)
    inicio = models.DateField(auto_now_add=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proyectos_vinculacion')

    class Meta:
        permissions = [
            ('view_proyecto_vinculacion', 'Puede acceder a Registro Vinculacion'),
            ('reporte_registro_proyectos', 'Puede acceder a reportes de Proyecto')
        ]

    def __unicode__(self):
        return '{}'.format(self.nombre)

class Componente(models.Model):
    proyecto_vinculacion = models.ForeignKey(Proyecto_vinculacion, on_delete=models.CASCADE, related_name='componentes')
    nombre = models.TextField(_(u'Nombre del Componente'))
    introduccion = models.TextField(_(u'Introduccion'), blank=True, null=True)
    observacion = models.TextField(_(u'Observaciones'), blank=True, null=True)
    inicio = models.DateField(_(u'Fecha de inicio'), blank=True, null=True)
    fin = models.DateField(_(u'Fecha de finalización'), blank=True, null=True)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='componentes', blank=True, null=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='componentes', blank=True, null=True)
    estado = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)], default=2)
    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        return '{}'.format(self.nombre)

class Objetivo(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='objectivos')
    nombre = models.TextField(_('Nombre'))

    def __unicode__(self):
        return '{}'.format(self.nombre)

class Actividad(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='actividades')
    nombre = models.TextField(_(u'Nombre de la Actividad'))
    realizado = models.TextField(_(u'Realizado'))
    meta = models.TextField(_(u'Meta'))
    resultado = models.TextField(_(u'Resultado'))
    cumplimiento = models.PositiveSmallIntegerField(_(u'% de Cumplimiento'), validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __unicode__(self):
        return '{}'.format(self.nombre)

class Recurso(models.Model):
    cantidad = models.PositiveSmallIntegerField(_(u'Cantidad'), validators=[MinValueValidator(0)])
    nombre = models.CharField(_(u'Nombre del Recurso'), max_length=50)
    descripcion = models.TextField(_(u'Descripcion'))
    unitario = models.FloatField(_(u'Valor Unitario'), validators=[MinValueValidator(0.00)])
    total = models.FloatField(_(u'Valor Total'), validators=[MinValueValidator(0.00)])

    def __unicode__(self):
        return '{}'.format(self.nombre)

    class Meta:
        abstract = True

class Recurso_humano(Recurso):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='recursos_humanos')

class Recurso_financiero(Recurso):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='recursos_financieros')

class Recurso_material(Recurso):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='recursos_materiales')

class Recurso_tecnologico(Recurso):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='recursos_tecnologicos')

class Evaluacion(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='evaluaciones', blank=True, null=True)
    actividad = models.ForeignKey(Actividad_vinculacion, on_delete=models.CASCADE, related_name='evaluaciones', blank=True, null=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='evaluaciones')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    total_horas = models.PositiveSmallIntegerField()
    puntualidad = models.FloatField(_(u'Puntualidad (1)'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    asistencia = models.FloatField(_(u'Asistencia (1)'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    actitud = models.FloatField(_(u'Actitud frente a actividades (2)'), validators=[MinValueValidator(0), MaxValueValidator(2)])
    cumplimiento = models.FloatField(_(u'Cumplimiento, Objetivos (2)'), validators=[MinValueValidator(0), MaxValueValidator(2)])
    aplicacion = models.FloatField(_(u'Aplicacion de habilidades y destreza (2)'), validators=[MinValueValidator(0), MaxValueValidator(2)])
    satisfaccion = models.FloatField(_(u'Nivel de satisfaccion (2)'), validators=[MinValueValidator(0), MaxValueValidator(2)])
    promedio = models.FloatField(_(u'Promedio'), validators=[MinValueValidator(0), MaxValueValidator(10)])

def generate_evidencia_proyecto(instance, filename):
    return 'proyectos/{0}/{1}'.format(instance.componente.slug, filename)

class Evidencia_proyecto(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='evidencias_proyecto')
    imagen = models.ImageField(upload_to=generate_evidencia_proyecto, max_length=200)

    def __unicode__(self):
        return '{}'.format(self.imagen.url)

###### / Proyecto vinculacion