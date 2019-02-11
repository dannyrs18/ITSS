# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Componente, Proyecto_vinculacion, Actividad_vinculacion
from ..registros.models import Estudiante
import time
from django.conf import settings

class ComponenteForm(forms.Form):
    nombre = forms.CharField(label=_(u'Nombre del Proyecto'), widget=forms.Textarea())
    creador = forms.CharField(label=_(u'Creador'))
    entidad = forms.CharField(label=_(u'Entidad Beneficiaria'))
    componente = forms.CharField(label=_(u'Nombre del Componente'), widget=forms.Textarea())
    responsable = forms.CharField(label=_(u'Responsable'))
    fecha = forms.CharField(label=_(u'Fecha'))
    
    def __init__(self, componente, user, *args, **kwargs):
        super(ComponenteForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control', 'readonly': 'readonly'})
        self.fields['nombre'].widget.attrs.update({'rows': 3})
        self.fields['nombre'].initial = u'{}'.format(componente.proyecto_vinculacion.nombre)
        self.fields['creador'].initial = u'{0} {1}'.format(componente.proyecto_vinculacion.responsable.first_name, componente.proyecto_vinculacion.responsable.last_name)
        self.fields['componente'].widget.attrs.update({'rows': 3})
        self.fields['entidad'].initial = u'{}'.format(componente.proyecto_vinculacion.entidad.nombre)
        self.fields['componente'].initial = u'{}'.format(componente.nombre)
        self.fields['responsable'].initial = u'{0} {1}'.format(user.first_name, user.last_name)
        self.fields['fecha'].initial = u'{}'.format(time.strftime("%d/%m/%y"))

class EstudianteForm(forms.Form):
    estudiante = forms.ModelChoiceField(label=_(u'Estudiante'), queryset=Estudiante.objects.all())

    def __init__(self, user, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        self.fields['estudiante'].widget.attrs.update({'class' : 'form-control search_select'})
        if user.has_perm('registros.resp_vinc'):
            self.fields['estudiante'].queryset = Estudiante.objects.filter(carrera=user.perfil.carrera)

class PeriodoRegistroForm(forms.Form):
    inicio = forms.DateField(label=_(u'Inicio de Periodo') ,input_formats=settings.DATE_INPUT_FORMATS)
    fin = forms.DateField(label=_(u'Culminación del periodo'), input_formats=settings.DATE_INPUT_FORMATS)

    def __init__(self, *args, **kwargs):
        super(PeriodoRegistroForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control fecha'})

    def clean(self, *args, **kwargs):
        cleaned_data = super(PeriodoRegistroForm, self).clean(*args, **kwargs)
        if cleaned_data.get('inicio') >= cleaned_data.get('fin'):
            self.add_error('fin', u'La fecha de culminacion debe ser mayor a la de inicio')

class AjaxChoiceField(forms.ChoiceField):
    def valid_value(self, value):
        return True

class ComponenteReporteForm(forms.Form):
    registro = forms.ModelChoiceField(queryset=Proyecto_vinculacion.objects.none())
    componente = AjaxChoiceField(choices=((None, '---------'),))
    reporte = AjaxChoiceField(choices=((None, '---------'),))

    def __init__(self, user, *args, **kwargs):
        super(ComponenteReporteForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control search_select'})
        if user.has_perm('registros.admin_vinc'):
            self.fields['registro'].queryset = Proyecto_vinculacion.objects.all()
        elif user.has_perm('registros.resp_vinc'):
            self.fields['registro'].queryset = Proyecto_vinculacion.objects.filter(carrera=user.perfil.carrera)

class ActividadReporteForm(forms.Form):
    registro = forms.ModelChoiceField(queryset=Actividad_vinculacion.objects.none())
    reporte = AjaxChoiceField(choices=((None, '---------'),))

    def __init__(self, user, *args, **kwargs):
        super(ActividadReporteForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control search_select'})
        if user.has_perm('registros.admin_vinc'):
            self.fields['registro'].queryset = Actividad_vinculacion.objects.all()
        elif user.has_perm('registros.resp_vinc'):
            self.fields['registro'].queryset = Actividad_vinculacion.objects.filter(carrera=user.perfil.carrera)