# coding: utf-8
import random
import string
import models

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from ..registros.models import Carrera

class ConvenioForm(forms.ModelForm):
    class Meta:
        model = models.Informe_vinculacion
        fields = '__all__'
        widgets = {'convenio': forms.FileInput(attrs={'class':'form-control'})}
    
    def save(self, commit=True):
        instance = super(ConvenioForm, self).save(commit=False)
        if models.Informe_vinculacion.objects.filter(pk=1):
            inf = models.Informe_vinculacion.objects.get(pk=1)
            inf.convenio = self.cleaned_data.get('convenio')
            inf.save()
        else:
            instance.save()

class EntidadForm(forms.ModelForm):
    inicio = forms.DateField(label=_(u'Fecha de Convenio'), input_formats=settings.DATE_INPUT_FORMATS)
    fin = forms.DateField(label=_(u'Finalización de Convenio'), input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = models.Entidad
        fields = ('nombre', 'encargado', 'cargo', 'correo', 'telefono', 'inicio', 'fin', 'direccion', 'descripcion', 'logo', 'carreras')
        labels = {'nombre': _(u'Nombre de la entidad')}
        widgets = {'carreras': forms.CheckboxSelectMultiple()}

    def __init__(self, user, *args, **kwargs):
        super(EntidadForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            if not key == 'carreras':
                self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'rows':5})
        self.fields['inicio'].widget.attrs.update({'class':'form-control fecha1'})
        self.fields['fin'].widget.attrs.update({'class':'form-control fecha2'})
        self.fields['direccion'].widget.attrs.update({'rows':3})
        if user.has_perm('registros.resp_vinc'):
            del self.fields['carreras']

    def save(self, user, commit=True):
        data = super(EntidadForm, self).save()
        data.responsable=user
        if user.has_perm('registros.resp_vinc'):
            data.carreras.add(user.perfil.carrera)
        data.save()
        return data

class EvidenciaEntidadForm(forms.Form):
    imagenes = forms.ImageField(label=_(u'Evidencia Fotografica'), widget=forms.FileInput(attrs={'class':"form-control", 'multiple': True}), required=True)

    def save(self, imagenes, entidad, commit=True):
        print imagenes
        for imagen in imagenes:
            print imagen
            models.Evidencias_Entidad.objects.create(entidad=entidad, imagen=imagen)

class ProyectoVinculacionForm(forms.ModelForm):
    class Meta:
        model = models.Proyecto_vinculacion
        fields = ('nombre', 'carrera', 'entidad',)

    def __init__(self, user, *args, **kwargs):
        super(ProyectoVinculacionForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows':3})
        self.fields['entidad'].widget.attrs.update({'class' : 'form-control search_select'})
        self.fields['carrera'].widget.attrs.update({'class' : 'form-control search_select'})
        if user.has_perm('registros.resp_vinc'):
            del self.fields['carrera']
            self.fields['entidad'].queryset = models.Entidad.objects.filter(carreras=user.perfil.carrera) # estado
        elif user.has_perm('registros.admin_vinc'):
            self.fields['entidad'].queryset = models.Entidad.objects.none()
            if self.data.get('carrera', ''):
                try:
                    carrera_id = self.data.get('carrera')
                    self.fields['entidad'].queryset = models.Entidad.objects.filter(carreras=carrera_id).order_by('nombre')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['entidad'].queryset = self.instance.carrera.entidades.order_by('nombre')

    def save(self, user, commit=True):
        data = super(ProyectoVinculacionForm, self).save(commit=False)
        data.responsable=user
        data.save()
        if user.has_perm('registros.resp_vinc'):
            data.carrera = user.perfil.carrera
        data.save()
        return data

class ComponenteForm(forms.ModelForm):
    class Meta:
        model = models.Componente
        fields = ('nombre', 'proyecto_vinculacion', )

    def __init__(self, *args, **kwargs):
        super(ComponenteForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows':2})
    
    def save(self, commit=True):
        instance = super(ComponenteForm, self).save()
        aleatorio = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
        instance.slug = '{0}{1}'.format(instance.id, aleatorio)
        instance.save()
        return instance

class RequiredFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

ComponenteFormSet = inlineformset_factory(models.Proyecto_vinculacion, models.Componente,
                                            form=ComponenteForm, formset=RequiredFormSet, can_delete=False, extra=3)
ComponenteFormSet2 = inlineformset_factory(models.Proyecto_vinculacion, models.Componente,
                                            form=ComponenteForm, extra=1)

class ObjetivoForm(forms.ModelForm):
    class Meta:
        model = models.Objetivo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ObjetivoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows':2})

ObjetivoFormSet = inlineformset_factory(models.Componente, models.Objetivo, form=ObjetivoForm, extra=1)

class ActividadForm(forms.ModelForm):
    class Meta:
        model = models.Actividad
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ActividadForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['nombre'].widget.attrs.update({'rows':2})

ActividadFormSet = inlineformset_factory(models.Componente, models.Actividad, form=ActividadForm, extra=1)
