# coding: utf-8
import random
import string
import models

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.forms import formset_factory
from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from ..registros.models import Carrera, Estudiante

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.DateInput):
    input_type = 'time'

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
    #inicio = forms.DateField(label=_(u'Fecha de Convenio'), input_formats=settings.DATE_INPUT_FORMATS)
    #fin = forms.DateField(label=_(u'Finalización de Convenio'), input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = models.Entidad
        fields = ('nombre', 'nombre_proyecto', 'encargado', 'cargo', 'correo', 'telefono', 'direccion', 'descripcion', 'logo', 'carreras')
        labels = {'nombre': _(u'Nombre de la entidad')}
        widgets = {'carreras': forms.CheckboxSelectMultiple()}

    def __init__(self, user, *args, **kwargs):
        super(EntidadForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            if not key == 'carreras':
                self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'rows':5})
        #self.fields['inicio'].widget.attrs.update({'class':'form-control fecha'})
        #self.fields['fin'].widget.attrs.update({'class':'form-control fecha'})
        self.fields['direccion'].widget.attrs.update({'rows':3})
        if user.has_perm('registros.resp_vinc'):
            del self.fields['carreras']

    #def clean(self, *args, **kwargs):
    #    cleaned_data = super(EntidadForm, self).clean(*args, **kwargs)
    #    if cleaned_data.get('inicio') >= cleaned_data.get('fin'):
    #        self.add_error('fin', u'La fecha de finalización debe ser mayor a la de inicio')

    def save(self, user, commit=True):
        from django.utils.timezone import localtime, now
        
        instance = super(EntidadForm, self).save()
        instance.responsable=user
        #if instance.fin > localtime(now()).date():
        #    instance.estado=True
        if user.has_perm('registros.resp_vinc'):
            instance.carreras.add(user.perfil.carrera)
        aleatorio = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
        instance.slug = '{0}{1}'.format(instance.id, aleatorio)
        instance.save()
        return instance

class ProyectoVinculacionForm(forms.ModelForm):
    class Meta:
        model = models.Proyecto_vinculacion
        fields = ('nombre', 'carrera', 'entidad',)
        widgets = {'nombre' : forms.Textarea()}

    def __init__(self, user, *args, **kwargs):
        super(ProyectoVinculacionForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows':3})
        self.fields['entidad'].widget.attrs.update({'class' : 'form-control search_select'})
        self.fields['carrera'].widget.attrs.update({'class' : 'form-control search_select'})
        if user.has_perm('registros.resp_vinc'):
            del self.fields['carrera']
            self.fields['entidad'].queryset = models.Entidad.objects.filter(carreras=user.perfil.carrera).exclude(fin=None) # estado
        elif user.has_perm('registros.admin_vinc'):
            self.fields['entidad'].queryset = models.Entidad.objects.none()
            if self.data.get('carrera', ''):
                try:
                    carrera_id = self.data.get('carrera')
                    self.fields['entidad'].queryset = models.Entidad.objects.filter(carreras=carrera_id).exclude(fin=None).order_by('nombre')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['entidad'].queryset = self.instance.carrera.entidades.order_by('nombre')

    def save(self, user, commit=True):
        data = super(ProyectoVinculacionForm, self).save(commit=False)
        data.responsable=user
        if user.has_perm('registros.resp_vinc'):
            data.carrera = user.perfil.carrera
        data.save()
        return data

class ComponenteForm(forms.ModelForm):
    class Meta:
        model = models.Componente
        fields = ('nombre', 'proyecto_vinculacion', )
        widgets = {'nombre' : forms.Textarea()}

    def __init__(self, *args, **kwargs):
        super(ComponenteForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows':2})
    
    def save(self, commit=True):
        instance = super(ComponenteForm, self).save()
        aleatorio = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
        instance.slug = '{0}{1}'.format(instance.id, aleatorio)
        instance.save()
        return instance

ComponenteFormSet = inlineformset_factory(models.Proyecto_vinculacion, models.Componente, form=ComponenteForm, extra=0, min_num=3)

class ObjetivoForm(forms.ModelForm):
    class Meta:
        model = models.Objetivo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ObjetivoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows':2})

ObjetivoFormSet = inlineformset_factory(models.Componente, models.Objetivo, form=ObjetivoForm, can_delete=True, extra=1)

class ActividadForm(forms.ModelForm):
    class Meta:
        model = models.Actividad
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ActividadForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control', 'rows':2})

ActividadFormSet = inlineformset_factory(models.Componente, models.Actividad, form=ActividadForm, can_delete=True, extra=1)

class RecursoHumanoForm(forms.ModelForm):
    class Meta:
        model = models.Recurso_humano
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RecursoHumanoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows':2})
        self.fields['descripcion'].widget.attrs.update({'class' : 'form-control', 'rows':2})
        self.fields['cantidad'].widget.attrs.update({'class' : 'form-control', 'onkeyup':"total(this.id, 'cantidad');"})
        self.fields['unitario'].widget.attrs.update({'class' : 'form-control', 'onkeyup':"total(this.id, 'cantidad');"})
        self.fields['total'].widget.attrs.update({'class' : 'form-control', 'readonly': "readonly"})

RecursoHumanoFormSet = inlineformset_factory(models.Componente, models.Recurso_humano, form=RecursoHumanoForm, can_delete=True, extra=1)

class RecursoFinancieroForm(forms.ModelForm):
    class Meta:
        model = models.Recurso_financiero
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RecursoFinancieroForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows':2})
        self.fields['descripcion'].widget.attrs.update({'class' : 'form-control', 'rows':2})
        self.fields['cantidad'].widget.attrs.update({'class' : 'form-control', 'onkeyup':"total(this.id, 'cantidad');"})
        self.fields['unitario'].widget.attrs.update({'class' : 'form-control', 'onkeyup':"total(this.id, 'cantidad');"})
        self.fields['total'].widget.attrs.update({'class' : 'form-control', 'readonly': "readonly"})

RecursoFinancieroFormSet = inlineformset_factory(models.Componente, models.Recurso_financiero, form=RecursoFinancieroForm, can_delete=True, extra=1)

class RecursoMaterialForm(forms.ModelForm):
    class Meta:
        model = models.Recurso_material
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RecursoMaterialForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows':2})
        self.fields['descripcion'].widget.attrs.update({'class' : 'form-control', 'rows':2})
        self.fields['cantidad'].widget.attrs.update({'class' : 'form-control', 'onkeyup':"total(this.id, 'cantidad');"})
        self.fields['unitario'].widget.attrs.update({'class' : 'form-control', 'onkeyup':"total(this.id, 'cantidad');"})
        self.fields['total'].widget.attrs.update({'class' : 'form-control', 'readonly': "readonly"})

RecursoMaterialFormSet = inlineformset_factory(models.Componente, models.Recurso_material, form=RecursoMaterialForm, can_delete=True, extra=1)

class RecursoTecnologicoForm(forms.ModelForm):
    class Meta:
        model = models.Recurso_tecnologico
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RecursoTecnologicoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows':2})
        self.fields['descripcion'].widget.attrs.update({'class' : 'form-control', 'rows':2})
        self.fields['cantidad'].widget.attrs.update({'class' : 'form-control', 'onkeyup':"total(this.id, 'cantidad');"})
        self.fields['unitario'].widget.attrs.update({'class' : 'form-control', 'onkeyup':"total(this.id, 'unitario');"})
        self.fields['total'].widget.attrs.update({'class' : 'form-control', 'readonly': "readonly"})

RecursoTecnologicoFormSet = inlineformset_factory(models.Componente, models.Recurso_tecnologico, form=RecursoTecnologicoForm, can_delete=True, extra=1)

class EvaluacionForm(forms.ModelForm):
    hora_entrada = forms.TimeField(widget=TimeInput)
    hora_salida = forms.TimeField(widget=TimeInput)
    fecha_inicio = forms.DateField(widget=DateInput)
    fecha_fin = forms.DateField(widget=DateInput)
    class Meta:
        mode = models.Evaluacion
        exclude = ('actividad', )
    
    def __init__(self, componente, *args, **kwargs):
        super(EvaluacionForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['puntualidad'].widget.attrs.update({'onkeyup':"asistencia(this.id, 'puntualidad');"})
        self.fields['asistencia'].widget.attrs.update({'onkeyup':"asistencia(this.id, 'asistencia');"})
        self.fields['actitud'].widget.attrs.update({'onkeyup':"asistencia(this.id, 'actitud');"})
        self.fields['cumplimiento'].widget.attrs.update({'onkeyup':"asistencia(this.id, 'cumplimiento');"})
        self.fields['aplicacion'].widget.attrs.update({'onkeyup':"asistencia(this.id, 'aplicacion');"})
        self.fields['satisfaccion'].widget.attrs.update({'onkeyup':"asistencia(this.id, 'satisfaccion');"})
        self.fields['promedio'].widget.attrs.update({'readonly' : 'readonly'})
        self.fields['estudiante'].queryset = Estudiante.objects.filter(carrera=componente.proyecto_vinculacion.carrera)

EvaluacionFormset = inlineformset_factory(models.Componente, models.Evaluacion, form=EvaluacionForm, can_delete=True, extra=1)

class EvidenciaProyectoForm(forms.Form):
    imagenes = forms.ImageField(label=_(u'Evidencia Fotografica'), widget=forms.FileInput(attrs={'class':"form-control", 'multiple': True}), required=True)

    def save(self, imagenes, componente):
        for imagen in imagenes:
            models.Evidencia_proyecto.objects.create(componente=componente, imagen=imagen)

class ActividadProyectoForm(forms.ModelForm):
    inicio = forms.DateField(label=_(u'Fecha de Convenio'), input_formats=settings.DATE_INPUT_FORMATS)
    fin = forms.DateField(label=_(u'Finalización de Convenio'), input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = models.Actividad_vinculacion
        fields = ('nombre', 'carrera', 'entidad', 'descripcion', 'justificacion', 'inicio', 'fin')

    def __init__(self, user, *args, **kwargs):
        super(ActividadProyectoForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['nombre'].widget.attrs.update({'rows' : 3})
        self.fields['justificacion'].widget.attrs.update({'rows' : 3})
        self.fields['descripcion'].widget.attrs.update({'rows' : 3})
        self.fields['inicio'].widget.attrs.update({'class' : 'form-control fecha'})
        self.fields['fin'].widget.attrs.update({'class' : 'form-control fecha'})
        self.fields['entidad'].widget.attrs.update({'class' : 'form-control search_select'})
        self.fields['carrera'].widget.attrs.update({'class' : 'form-control search_select'})
        if user.has_perm('registros.resp_vinc'):
            del self.fields['carrera']
            self.fields['entidad'].queryset = models.Entidad.objects.filter(carreras=user.perfil.carrera).exclude(fin=None) # estado
        elif user.has_perm('registros.admin_vinc'):
            self.fields['entidad'].queryset = models.Entidad.objects.none()
            if self.data.get('carrera', ''):
                try:
                    carrera_id = self.data.get('carrera')
                    self.fields['entidad'].queryset = models.Entidad.objects.filter(carreras=carrera_id).exclude(fin=None).order_by('nombre')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['entidad'].queryset = self.instance.carrera.entidades.order_by('nombre')

    def save(self, user, commit=True):
        data = super(ActividadProyectoForm, self).save(commit=False)
        data.responsable=user
        if user.has_perm('registros.resp_vinc'):
            data.carrera = user.perfil.carrera
        data.save()
        return data

class ObjetivoEspecificoForm(forms.ModelForm):
    class Meta:
        model = models.Objetivo_Especifico
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ObjetivoEspecificoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows': 3})

# ObjetivoEspecificoFormset = inlineformset_factory(models.Actividad_vinculacion, models.Objetivo_Especifico, form=ObjetivoEspecificoForm, extra=1)
ObjetivoEspecificoFormset = inlineformset_factory(models.Actividad_vinculacion, models.Objetivo_Especifico, form=ObjetivoEspecificoForm, can_delete=True, extra=1)

class ObjetivoGeneralForm(forms.ModelForm):
    class Meta:
        model = models.Objetivo_General
        fields = ('nombre',)

    def __init__(self, *args, **kwargs):
        super(ObjetivoGeneralForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows': 3})

ObjetivoGeneralFormset = inlineformset_factory(models.Actividad_vinculacion, models.Objetivo_General, form=ObjetivoGeneralForm, can_delete=True, extra=1)

class ActividadAcForm(forms.ModelForm):
    class Meta:
        model = models.Actividad_Ac
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ActividadAcForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control', 'rows': 3})

ActividadAcFormset = inlineformset_factory(models.Actividad_vinculacion, models.Actividad_Ac, form=ActividadAcForm, extra=1)

class Evaluacion2Form(forms.ModelForm):
    hora_entrada = forms.TimeField(widget=TimeInput)
    hora_salida = forms.TimeField(widget=TimeInput)
    fecha_inicio = forms.DateField(widget=DateInput)
    fecha_fin = forms.DateField(widget=DateInput)
    class Meta:
        mode = models.Evaluacion
        exclude = ('componente', )
    
    def __init__(self, user, carrera, *args, **kwargs):
        self.carrera = carrera
        super(Evaluacion2Form, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['puntualidad'].widget.attrs.update({'onkeyup':"asistencia(this.id, 'puntualidad');"})
        self.fields['asistencia'].widget.attrs.update({'onkeyup':"asistencia(this.id, 'asistencia');"})
        self.fields['actitud'].widget.attrs.update({'onkeyup':"asistencia(this.id, 'actitud');"})
        self.fields['cumplimiento'].widget.attrs.update({'onkeyup':"asistencia(this.id, 'cumplimiento');"})
        self.fields['aplicacion'].widget.attrs.update({'onkeyup':"asistencia(this.id, 'aplicacion');"})
        self.fields['satisfaccion'].widget.attrs.update({'onkeyup':"asistencia(this.id, 'satisfaccion');"})
        self.fields['promedio'].widget.attrs.update({'readonly' : 'readonly'})
        if user.has_perm('registros.resp_vinc'):
            self.fields['estudiante'].queryset = Estudiante.objects.filter(carrera=user.perfil.carrera)

    def clean(self, *args, **kwargs):
        cleaned_data = super(Evaluacion2Form, self).clean(*args, **kwargs)
        if self.carrera:
            if not cleaned_data.get('estudiante').carrera.id == int(self.carrera):
                self.add_error('estudiante', u'El estudiante no pertenece a la carrera')
                print 'True'
        if cleaned_data.get('fecha_inicio') >= cleaned_data.get('fecha_fin'):
            self.add_error('fecha_fin', u'La fecha de finalización debe ser mayor a la de inicio')

Evaluacion2Formset = inlineformset_factory(models.Actividad_vinculacion, models.Evaluacion, form=Evaluacion2Form, extra=1)

class EvidenciaActividadForm(forms.Form):
    imagenes = forms.ImageField(label=_(u'Evidencia Fotografica'), widget=forms.FileInput(attrs={'class':"form-control", 'multiple': True}), required=True)

    def save(self, imagenes, actividad):
        for imagen in imagenes:
            models.Evidencia_actividad.objects.create(actividad=actividad, imagen=imagen)