# coding: utf-8
import random
import string
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Perfil

class PasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})

class UserPerfilForm(forms.ModelForm):
    first_name = forms.CharField(label=_(u'Nombres'))
    last_name = forms.CharField(label=_(u'Apellidoss'))
    cedula = forms.CharField(label=_(u'Cedula'))
    telefono = forms.CharField(label=_(u'Telefono'))
    email = forms.EmailField(label=_(u'Email'))
    class Meta:
        model = Perfil
        fields = ('docente','first_name', 'last_name', 'cedula', 'telefono', 'avatar')

    def __init__(self, *args, **kwargs):
        super(UserPerfilForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['docente'].widget.attrs.update({'class' : 'form-control search_select'})
        self.fields['first_name'].widget.attrs.update({'readonly' : 'readonly'})
        self.fields['last_name'].widget.attrs.update({'readonly' : 'readonly'})
        self.fields['cedula'].widget.attrs.update({'readonly' : 'readonly'})
        self.fields['telefono'].widget.attrs.update({'readonly' : 'readonly'})
        if self.instance.user.email:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        instance = super(UserPerfilForm, self).save()
        instance.refresh_from_db()  # cargar la instancia de perfil creada por la señal
        instance.user.first_name = instance.docente.nombres
        instance.user.last_name = instance.docente.apellidos
        instance.user.email = self.cleaned_data.get('email')
        instance.user.save()
        if not instance.slug:
            aleatorio = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
            instance.slug = '{0}{1}'.format(instance.id, aleatorio)
        instance.save()
        #self.send_email(self.cleaned_data)
        return instance

    def send_email(self, data):
        from django.core.mail import EmailMessage

        data = self.cleaned_data
        mensaje = u"""Correo de Confirmación.
        Su cuenta ha sido modificada exitosamente"""
        mail = EmailMessage('Instituto tecnologico Superior Sudamericano', mensaje, to=[data.get('email')])
        mail.send()