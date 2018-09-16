# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
"""
class AdminForm(UserCreationForm):

    PRACTICAS = 'practicas'
    VINCULACION = 'vinculacion'
    SELECT = (
        (None, '-------'),
        (PRACTICAS,_(u'ADMINISTRAR PRACTICAS')),
        (VINCULACION, _(u'ADMINISTRAR VINCULACIÓN')),
    )
    tipo = forms.ChoiceField(choices=SELECT, widget= forms.Select(attrs={'class':'form-control js-example-basic-single'}))
    avatar = forms.ImageField(label=_('Imagen de perfil'), widget = forms.FileInput(attrs={'class':'form-control'}), required=False)
    docente = forms.ModelChoiceField(queryset=Docentes.objects.all(), widget= forms.Select(attrs={'class':'form-control js-example-basic-single'}))
    cedula = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
    class Meta:
"""
class RootForm(UserCreationForm):

    PRACTICAS, VINCULACION = 1, 2
    SELECT = (
        (None, '-----'),
        (PRACTICAS,_(u'PRACTICAS')),
        (VINCULACION, _(u'VINCULACIÓN')),   
    )

    username = forms.CharField(max_length='20', label=_('Usuario'))
    avatar = forms.ImageField(_('Imagen de perfil'))
    cedula = forms.IntegerField(_('Cedula'))
    admin = forms.ChoiceField(choices=SELECT, label=_('Administracion'))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'cedula', 'email', 'avatar', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RootForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['cedula'].widget.attrs.update({'class' : 'form-control'})
        self.fields['avatar'].widget.attrs.update({'class' : 'form-control', 'required':False})
        self.fields['password1'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password2'].widget.attrs.update({'class' : 'form-control'})


    def grupo():
        pass