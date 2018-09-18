# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django import forms
from .models import Informe_practicas, Empresa, Registro
from ..registros.models import Carrera, Estudiante

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
    inicio = forms.DateField(label=_(u'Inicio de Convenio') ,input_formats=settings.DATE_INPUT_FORMATS)
    fin = forms.DateField(label=_(u'Finalización de Convenio'), input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Empresa
        fields = ('nombre', 'gerente', 'correo', 'telefono', 'inicio', 'fin', 'direccion', 'descripcion', 'logo')
        labels = {'nombre': _(u'Nombre de la empresa')}

    def __init__(self, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class' : 'form-control', 'rows':3})
        self.fields['descripcion'].widget.attrs.update({'class' : 'form-control', 'rows':3})
        self.fields['inicio'].widget.attrs.update({'class' : 'form-control fecha1'})
        self.fields['fin'].widget.attrs.update({'class' : 'form-control fecha2'})

    def clean(self, *args, **kwargs):
        instance = super(EmpresaForm, self).clean(*args, **kwargs)
        estudiante = instance.get('estudiante', None)
        if estudiante:
            if estudiante.practicas.filter(estado=True).exists():
                self.add_error('estudiante', 'El estudiantes se encuentra actualmente en otro proceso de practicas')

    def save(self, user, commit=True):
        from django.utils.timezone import localtime, now
        from datetime import datetime

        instance = super(EmpresaForm, self).save(commit=False)
        instance.usuario=user
        if localtime(now()).date() >= instance.inicio and localtime(now()).date() < instance.fin:
            instance.estado = True
        instance.save()
        if user.has_perm('registros.admin_prac'):
            instance.carreras = Carrera.objects.all()
        elif user.has_perm('registros.resp_prac'):
            instance.carreras.add(user.perfil.carrera)
        instance.save()

class RegistroForm(forms.ModelForm):
    nombres = forms.CharField(label=_(u'Nombres'))
    apellidos = forms.CharField(label=_(u'Apellidos'))
    cedula = forms.IntegerField(label=_(u'cedula'))
    presentacion = forms.DateField(label=_(u'Fecha de Presentación') ,input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Registro
        fields = ('estudiante', 'nombres', 'apellidos', 'cedula', 'empresa', 'presentacion', 'solicitud', 'aceptacion')

        widgets = {
            'estudiante': forms.Select(attrs={'class':"form-control js-example-basic-single"}),
            'empresa': forms.Select(attrs={'class':"form-control js-example-basic-single"}),
            'presentacion': forms.TextInput(attrs={'class':'form-control fecha1'}),
            'solicitud': forms.FileInput(attrs={'class':"form-control"}),
            'aceptacion': forms.FileInput(attrs={'class':"form-control"}),
        }
        
    def __init__(self, user, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['empresa'].queryset = Empresa.objects.filter(estado=True, carreras=user.perfil.carrera)
        self.fields['estudiante'].queryset = Estudiante.objects.filter(carrera=user.perfil.carrera)
        self.fields['nombres'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        self.fields['apellidos'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        self.fields['cedula'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})

    def clean(self, *args, **kwargs):
        instance = super(RegistroForm, self).clean(*args, **kwargs)
        estudiante = instance.get('estudiante', None)
        if estudiante.practicas.filter(estado=True).exists():
            self.add_error('estudiante', 'El estudiantes se encuentra actualmente en otro proceso de practicas')

    def save(self, user, commit=True):
        instance = super(RegistroForm, self).save(commit=False)
        instance.carrera = user.perfil.carrera
        instance.save()