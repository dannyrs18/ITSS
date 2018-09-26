# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Componente, Objetivo

class ComponenteForm(forms.ModelForm):
    introduccion = forms.CharField(label=_(u'Introducción'), widget=forms.Textarea())
    observaciones = forms.CharField(label=_(u'Observaciones'), widget=forms.Textarea())
    class Meta:
        model = Componente
        fields = ('introduccion', 'observaciones')

    def __init__(self, componente, *args, **kwargs):
        super(ComponenteForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control', 'rows': 4})