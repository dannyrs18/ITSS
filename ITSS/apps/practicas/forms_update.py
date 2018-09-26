# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from .models import Registro_practicas
from django.conf import settings
from django import forms

# Se crea variables auxiliares con el proposito de no habilitar el campo que acceda a la variable a modificar en la plantilla
# y muestre campos que no afecten a la base de datos
class RegistroForm(forms.ModelForm):
    aux_nombre = forms.CharField(label=_(u'Nombre del Estudiante'))
    aux_empresa = forms.CharField(label=_(u'Empresa'))
    fin = forms.DateField(label=_(u'Fecha de Culminación'), input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Registro_practicas
        fields = ('aux_nombre' , 'aux_empresa', 'horas', 'fin', 'calificacion')

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['fin'].widget.attrs.update({'class':'form-control fecha1'})
        self.fields['aux_nombre'].widget.attrs.update({'readonly': 'readonly'})
        self.fields['aux_empresa'].widget.attrs.update({'readonly': 'readonly'})
        self.fields['aux_nombre'].initial = kwargs['instance'].estudiante.get_full_name()
        self.fields['aux_empresa'].initial = kwargs['instance'].empresa.nombre

    def save(self, commit=True):
        instance = super(RegistroForm, self).save(commit=True)
        instance.estado = False
        instance.save()
        return instance