# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Componente
import time

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