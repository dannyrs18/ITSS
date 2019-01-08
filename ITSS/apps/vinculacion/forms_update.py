# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Componente, Objetivo
from django.conf import settings
import models

class ComponenteForm(forms.ModelForm):
    inicio = forms.DateField(label=_(u'Fecha de Inicio'), input_formats=settings.DATE_INPUT_FORMATS)
    fin = forms.DateField(label=_(u'Fecha de Finalización'), input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = models.Componente
        fields = ('inicio', 'fin', 'introduccion', 'observacion', 'seccion')
        help_texts = {'hora_inicio': 'Formato 24 horas', 'hora_fin': 'Formato 24 horas'}

    def __init__(self, *args, **kwargs):
        super(ComponenteForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control', 'rows': 3})
        self.fields['inicio'].widget.attrs.update({'class': 'form-control fecha'})
        self.fields['fin'].widget.attrs.update({'class': 'form-control fecha'})

    def clean(self, *args, **kwargs):
        cleaned_data = super(ComponenteForm, self).clean(*args, **kwargs)
        if self.instance.proyecto_vinculacion.inicio >= cleaned_data.get('inicio'):
            self.add_error('inicio', u'La fecha debe ser mayor a la fecha de inicio del proyecto')
        elif cleaned_data.get('inicio') >= cleaned_data.get('fin'):
            self.add_error('fin', u'La fecha de finalización debe ser mayor a la de inicio')

    def save(self, user, commit=True):
        instance = super(ComponenteForm, self).save()
        instance.responsable = user
        instance.estado = 0
        if instance.id == instance.proyecto_vinculacion.componentes.last().id:
            instance.proyecto_vinculacion.estado=0
            instance.proyecto_vinculacion.save()
        instance.save()
        return instance

class EntidadForm(forms.ModelForm):
    aux_nombre = forms.CharField(label=_(u'Nombre de la entidad'))
    class Meta:
        model = models.Entidad
        fields = ('aux_nombre', 'encargado', 'cargo', 'telefono', 'correo', 'direccion', 'logo')

    def __init__(self, *args, **kwargs):
        super(EntidadForm, self).__init__(*args, **kwargs)
        entidad = kwargs['instance']
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['direccion'].widget.attrs.update({'rows' : 3})
        self.fields['aux_nombre'].widget.attrs.update({'readonly' : 'readonly'})
        self.fields['aux_nombre'].initial = entidad.nombre

class EntidadProcesoForm(forms.ModelForm):
    aux_nombre = forms.CharField(label=_(u'Nombre de la entidad'))
    aux_responsable = forms.CharField(label=_(u'Responsable'))
    inicio = forms.DateField(label=_(u'Finalización de Convenio'), input_formats=settings.DATE_INPUT_FORMATS)
    fin = forms.DateField(label=_(u'Finalización de Convenio'), input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = models.Entidad
        fields = ('aux_nombre', 'aux_responsable', 'inicio', 'fin')

    def clean(self, *args, **kwargs):
        cleaned_data = super(EntidadProcesoForm, self).clean(*args, **kwargs)
        if cleaned_data.get('inicio') >= cleaned_data.get('fin'):
            self.add_error('fin', u'La fecha de finalización incorrecta')

    def __init__(self, *args, **kwargs):
        super(EntidadProcesoForm, self).__init__(*args, **kwargs)
        entidad = kwargs['instance']
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['inicio'].widget.attrs.update({'class' : 'form-control fecha', 'required':True})
        self.fields['fin'].widget.attrs.update({'class' : 'form-control fecha', 'required':True})
        self.fields['aux_nombre'].widget.attrs.update({'readonly' : 'readonly'})
        self.fields['aux_responsable'].widget.attrs.update({'readonly' : 'readonly'})
        self.fields['aux_nombre'].initial = entidad.nombre
        self.fields['aux_responsable'].initial = entidad.encargado

    def save(self, commit=True):
        from django.utils.timezone import localtime, now
        
        instance = super(EntidadProcesoForm, self).save()
        if instance.fin > localtime(now()).date():
            instance.estado=True
        instance.save()
        return instance

class EvidenciaEntidadForm(forms.Form):
    imagenes = forms.ImageField(label=_(u'Evidencia Fotografica'), widget=forms.FileInput(attrs={'class':"form-control", 'multiple': True}), required=True)

    def save(self, imagenes, entidad, commit=True):
        print imagenes
        for imagen in imagenes:
            print imagen
            models.Evidencias_Entidad.objects.create(entidad=entidad, imagen=imagen)