from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Informe_vinculacion, Entidad
from ..registros.models import Carrera

class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Informe_vinculacion
        fields = '__all__'
        widgets = {
            'convenio': forms.FileInput(attrs={'class':'form-control'}),
        }
    
    def save(self, commit=True):
        instance = super(ConvenioForm, self).save(commit=False)
        if Informe_vinculacion.objects.filter(pk=1):
            inf = Informe_vinculacion.objects.get(pk=1)
            inf.convenio = self.cleaned_data.get('convenio')
            inf.save()
        else:
            instance.save()

class EntidadForm(forms.ModelForm):
    class Meta:
        model = Entidad
        fields = ('nombre', 'responsable', 'cargo', 'correo', 'telefono', 'inicio', 'fin', 'direccion', 'descripcion', 'logo', 'carreras')
        widgets = {'carreras': forms.CheckboxInput()}
        labels = {'nombre': _(u'Nombre de la entidad')}

    def __init__(self, *args, **kwargs):
        super(EntidadForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'rows':5})
        self.fields['direccion'].widget.attrs.update({'rows':3})

    def save(self, user, commit=True):
        data = super(EntidadForm, self).save(commit=False)
        data.usuario=user
        if user.has_perm('registros.admin_prac'):
            data.carreras = Carrera.objects.all()
        elif user.has_perm('registros.resp_prac'):
            data.carreras.add(user.perfil.carrera)
        data.save()
        return data