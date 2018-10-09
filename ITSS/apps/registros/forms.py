from django import forms
from django.utils.translation import ugettext_lazy as _

class ErrorForm(forms.Form):
    tipo = forms.CharField(label=_(u'Problema presentado'))
    detalle = forms.CharField(label=_(u'Detalle el problema'), widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(ErrorForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['detalle'].widget.attrs.update({'rows' : 4})

    def save(self, user):
        from django.core.mail import EmailMessage

        responsable = ''
        if user.perfil.docente:
            responsable = u'{}'.format(user.perfil.docente.get_full_name())
        else:
            responsable = 'Administrador'
        data = self.cleaned_data
        mensaje = u"""
        Tipo de error: {}
        Detalle del error: {}
        Enviado por: {}""".format(data.get('tipo'), data.get('detalle'), responsable)
        mail = EmailMessage('Instituto tecnologico Superior Sudamericano', mensaje, to=['dannyors18@gmail.com'])
        mail.send()