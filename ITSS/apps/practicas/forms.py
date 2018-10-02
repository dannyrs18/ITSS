from django.utils.translation import ugettext_lazy as _
from django import forms
from ..registros.models import Estudiante

class EstudianteForm(forms.Form):
    estudiante = forms.ModelChoiceField(label=_(u'Estudiante'), queryset=Estudiante.objects.all())

    def __init__(self, user, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        self.fields['estudiante'].widget.attrs.update({'class' : 'form-control search_select'})
        if user.perfil.carrera:
            self.fields['estudiante'].queryset = Estudiante.objects.filter(carrera=user.perfil.carrera)