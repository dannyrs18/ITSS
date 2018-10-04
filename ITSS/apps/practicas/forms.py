# coding: utf8
from django.conf import settings
from django import forms
from ..registros.models import Estudiante
from django.utils.translation import ugettext_lazy as _

class EstudianteForm(forms.Form):
    estudiante = forms.ModelChoiceField(label=_(u'Estudiante'), queryset=Estudiante.objects.all())

    def __init__(self, user, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        self.fields['estudiante'].widget.attrs.update({'class' : 'form-control search_select'})
        if user.has_perm('registros.resp_prac'):
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