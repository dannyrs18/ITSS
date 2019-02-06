# coding: utf-8

import random
import string

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django import forms
from .models import Informe_practicas, Empresa, Registro_practicas, Evidencias_Empresa, Evidencias_registro_practicas
from ..registros.models import Carrera, Estudiante
from django.utils.timezone import localtime, now

class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Informe_practicas
        fields = '__all__'
        widgets = {
            'convenio': forms.FileInput(attrs={'class':'form-control'}),
        }
    
    def save(self, commit=True):
        instance = super(ConvenioForm, self).save(commit=False)
        if Informe_practicas.objects.filter(pk=1):
            inf = Informe_practicas.objects.get(pk=1)
            inf.convenio = self.cleaned_data.get('convenio')
            inf.save()
        else:
            instance.save()

class EmpresaForm(forms.ModelForm):
    telefono = forms.IntegerField(label=_(u'Telefono'))
    class Meta:
        model = Empresa
        fields = ('nombre', 'gerente', 'cargo', 'correo', 'telefono', 'direccion', 'descripcion', 'logo', 'carreras')
        labels = {'nombre': _(u'Nombre de la empresa')}
        widgets = {'carreras': forms.CheckboxSelectMultiple()}
    def __init__(self, user, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            if not key == 'carreras':
                self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class' : 'form-control', 'rows':3})
        self.fields['descripcion'].widget.attrs.update({'class' : 'form-control', 'rows':5})
        if not user.has_perm('registros.admin_prac'):
            del self.fields['carreras']

    def save(self, user, commit=True):
        from django.utils.timezone import localtime, now

        instance = super(EmpresaForm, self).save()
        instance.responsable=user
        instance.save()
        aleatorio = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
        instance.slug = '{0}{1}'.format(instance.id, aleatorio)
        if user.has_perm('registros.resp_prac'):
            instance.carreras.add(user.perfil.carrera)
        instance.save()
        return instance

class RegistroForm(forms.ModelForm):
    nombres = forms.CharField(label=_(u'Nombres'))
    apellidos = forms.CharField(label=_(u'Apellidos'))
    cedula = forms.IntegerField(label=_(u'cedula'))
    presentacion = forms.DateField(label=_(u'Fecha de Presentación') ,input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Registro_practicas
        fields = ('carrera', 'estudiante', 'nombres', 'apellidos', 'cedula', 'empresa', 'presentacion', 'carrera')
        widgets = {
            'estudiante': forms.Select(attrs={'class':"form-control search_select"}),
            'empresa': forms.Select(attrs={'class':"form-control search_select"}),
            'carrera': forms.Select(attrs={'class':"form-control search_select"}),
        }
        
    def __init__(self, user, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['nombres'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        self.fields['apellidos'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        self.fields['cedula'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        self.fields['presentacion'].widget.attrs.update({'class' : 'form-control fecha'})
        if user.has_perm('registros.resp_prac'):
            self.fields['empresa'].queryset = Empresa.objects.filter(carreras=user.perfil.carrera, estado=True)
            self.fields['estudiante'].queryset = Estudiante.objects.filter(carrera=user.perfil.carrera)
            del self.fields['carrera']
        else:
            self.fields['empresa'].queryset = Empresa.objects.none()
            self.fields['estudiante'].queryset = Estudiante.objects.none()
            if self.data.get('carrera'):
                try:
                    carrera_id = self.data.get('carrera')
                    self.fields['empresa'].queryset = Empresa.objects.filter(carreras=carrera_id).order_by('nombre')
                    self.fields['estudiante'].queryset = Estudiante.objects.filter(carrera=carrera_id).order_by('nombres')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['empresa'].queryset = self.instance.carrera.empresas.order_by('nombre')
                self.fields['estudiante'].queryset = self.instance.carrera.estudiantes.order_by('nombres')

    def clean(self, *args, **kwargs):
        instance = super(RegistroForm, self).clean(*args, **kwargs)
        estudiante = instance.get('estudiante', None)
        if estudiante.registros_practicas.filter(estado=True).exists():
            self.add_error('estudiante', 'El estudiantes se encuentra actualmente en otro proceso de practicas')

    def save(self, user, commit=True):
        instance = super(RegistroForm, self).save(commit=False)
        if user.has_perm('registros.resp_prac'):
            instance.carrera = user.perfil.carrera
        instance.save()
        aleatorio = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
        instance.slug = '{0}{1}'.format(instance.id, aleatorio)
        instance.save()
        return instance

class EvidenciaRegistroForm(forms.Form):
    imagenes = forms.ImageField(label=_(u'Evidencia Fotografica'), widget=forms.FileInput(attrs={'class':"form-control", 'multiple': True}), required=True)

    def save(self, imagenes, registro_practicas, commit=True):
        print imagenes
        for imagen in imagenes:
            print imagen
            Evidencias_registro_practicas.objects.create(registro_practicas=registro_practicas, imagen=imagen)