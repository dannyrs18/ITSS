# coding: utf-8
from django.utils.translation import ugettext_lazy as _
import models
from django.conf import settings
from django import forms

# Se crea variables auxiliares con el proposito de no habilitar el campo que acceda a la variable a modificar en la plantilla
# y muestre campos que no afecten a la base de datos
class RegistroForm(forms.ModelForm):
    aux_nombre = forms.CharField(label=_(u'Nombre del Estudiante'))
    aux_empresa = forms.CharField(label=_(u'Empresa'))
    fin = forms.DateField(label=_(u'Fecha de Culminación'), input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = models.Registro_practicas
        fields = ('aux_nombre' , 'aux_empresa', 'horas', 'fin', 'calificacion')

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['fin'].widget.attrs.update({'class':'form-control fecha'})
        self.fields['aux_nombre'].widget.attrs.update({'readonly': 'readonly'})
        self.fields['aux_empresa'].widget.attrs.update({'readonly': 'readonly'})
        self.fields['aux_nombre'].initial = kwargs['instance'].estudiante.get_full_name()
        self.fields['aux_empresa'].initial = kwargs['instance'].empresa.nombre

    def clean(self, *args, **kwargs):
        cleaned_data = super(RegistroForm, self).clean(*args, **kwargs)
        if cleaned_data.get('fin') < self.instance.presentacion:
            self.add_error('fin', u'La fecha de culminación debe ser mayor a la de presentación')

    def save(self, commit=True):
        instance = super(RegistroForm, self).save(commit=True)
        instance.estado = False
        instance.save()
        return instance

class EmpresaForm(forms.ModelForm):
    aux_nombre = forms.CharField(label=_(u'Nombre de la empresa'))

    class Meta:
        model = models.Empresa
        fields = ('aux_nombre', 'gerente', 'cargo', 'telefono', 'correo', 'direccion', 'logo')

    def __init__(self, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)
        empresa = kwargs['instance']
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['direccion'].widget.attrs.update({'rows' : 3})
        self.fields['aux_nombre'].widget.attrs.update({'readonly' : 'readonly'})
        self.fields['aux_nombre'].initial = empresa.nombre

class EmpresaProcesoForm(forms.ModelForm):
    aux_nombre = forms.CharField(label=_(u'Nombre de la empresa'))
    aux_gerente = forms.CharField(label=_(u'Gerente'))
    inicio = forms.DateField(label=_(u'Inicio de Convenio'), input_formats=settings.DATE_INPUT_FORMATS)
    fin = forms.DateField(label=_(u'Finalización de Convenio'), input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = models.Empresa
        fields = ('aux_nombre', 'aux_gerente', 'inicio', 'fin')

    def clean(self, *args, **kwargs):
        cleaned_data = super(EmpresaProcesoForm, self).clean(*args, **kwargs)
        if cleaned_data.get('inicio') >= cleaned_data.get('fin'):
            self.add_error('fin', u'La fecha de finalización incorrecta')

    def __init__(self, *args, **kwargs):
        super(EmpresaProcesoForm, self).__init__(*args, **kwargs)
        empresa = kwargs['instance']
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['inicio'].widget.attrs.update({'class' : 'form-control fecha'})
        self.fields['fin'].widget.attrs.update({'class' : 'form-control fecha'})
        self.fields['aux_nombre'].widget.attrs.update({'readonly' : 'readonly'})
        self.fields['aux_gerente'].widget.attrs.update({'readonly' : 'readonly'})
        self.fields['aux_nombre'].initial = empresa.nombre
        self.fields['aux_gerente'].initial = empresa.gerente

    def save(self, commit=True):
        from django.utils.timezone import localtime, now
        
        instance = super(EmpresaProcesoForm, self).save()
        if instance.fin > localtime(now()).date():
            instance.estado=True
            instance.save()
        return instance

class EvidenciaEmpresaForm(forms.Form):
    imagenes = forms.ImageField(label=_(u'Evidencia Fotografica'), widget=forms.FileInput(attrs={'class':"form-control", 'multiple': True}), required=True)

    def save(self, imagenes, empresa, commit=True):
        print imagenes
        for imagen in imagenes:
            print imagen
            models.Evidencias_Empresa.objects.create(empresa=empresa, imagen=imagen)