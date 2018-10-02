# -*- coding: utf-8 -*-
import random
import string

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Permission
from .models import Docente, Carrera
from ..modulos import permisos

class UserForm(UserCreationForm):

    PRACTICAS, VINCULACION = 1, 2
    SELECT = (
        (None, '---------'),
        (PRACTICAS,_(u'PRACTICAS')),
        (VINCULACION, _(u'VINCULACIÓN')),
    )
    admin = forms.ChoiceField(choices=SELECT, label=_('Administracion'))
    carrera = forms.ModelChoiceField(label=_('Carrera'), queryset=Carrera.objects.all())
    docente = forms.ModelChoiceField(label=_('Docente'), queryset=Docente.objects.all())
    cedula = forms.IntegerField(label=_('Cedula'))
    telefono = forms.CharField(label=_('Telefono'))
    avatar = forms.ImageField(label=_('Imagen de perfil'), required=False)

    class Meta:
        model = User
        fields = ('admin', 'carrera', 'docente', 'first_name', 'last_name', 'cedula', 'telefono', 'email', 'avatar', 'username', 'password1', 'password2')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['carrera'].widget.attrs.update({'class' : 'form-control search_select'})
        self.fields['docente'].widget.attrs.update({'class' : 'form-control search_select'})
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        self.fields['cedula'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        self.fields['telefono'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        if not user.is_superuser:
            del self.fields['admin']
        else:
            del self.fields['carrera']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        docente = cleaned_data.get('docente')
        user = self.user
        if user.is_superuser:
            if cleaned_data.get('admin') == '1':
                for value in Permission.objects.get(codename='admin_prac').user_set.all():
                    if docente == value.perfil.docente:
                        msg = "El docente ya contiene una cuenta de practicas, posiblemente deba activarla"
                        self.add_error('docente', msg)
            elif cleaned_data.get('admin') == '2':
                for value in Permission.objects.get(codename='admin_vinc').user_set.all():
                    if docente == value.perfil.docente:
                        msg = "El docente ya contiene una cuenta de vinculación, posiblemente deba activarla"
                        self.add_error('docente', msg)
        elif user.has_perm('registros.admin_prac'):
            carrera = cleaned_data.get('carrera')
            for value in Permission.objects.get(codename='resp_prac').user_set.all():
                if docente == value.perfil.docente and carrera == value.perfil.carrera:
                    msg = "El docente ya contiene una cuenta, posiblemente deba activarla"
                    self.add_error('docente', msg)
        elif user.has_perm('registros.admin_vinc'):
            carrera = cleaned_data.get('carrera')
            for value in Permission.objects.get(codename='resp_vinc').user_set.all():
                if docente == value.perfil.docente and carrera == value.perfil.carrera:
                    msg = "El docente ya contiene una cuenta, posiblemente deba activarla"
                    self.add_error('docente', msg)


    def save(self, commit=True):
        user = self.user
        instance = super(UserForm, self).save(commit=True)
        instance.refresh_from_db()  # cargar la instancia de perfil creada por la señal
        self.perms(user, instance)
        if self.cleaned_data.get('carrera', ''):
            instance.perfil.carrera = self.cleaned_data.get('carrera', '')
        if commit:
            instance.perfil.docente = self.cleaned_data.get('docente', '')
            instance.perfil.avatar = self.cleaned_data.get('avatar')
            aleatorio = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
            instance.perfil.slug = '{0}{1}'.format(instance.id, aleatorio)
            instance.save()
            self.estado(user, instance)
            #self.send_email(self.cleaned_data)
        return instance

    def perms(self, user, instance):
        if user.is_superuser: # Si es super usuario entonce registrara un administrador ya sea de practicas o vinculacion
            if self.cleaned_data.get('admin') == '1':
                instance.user_permissions = permisos.administrador_practicas()
            elif self.cleaned_data.get('admin') == '2':
                instance.user_permissions = permisos.administrador_vinculacion()
        elif user.has_perm('registros.admin_prac'): # Caso contrario es un administrador de practicas y registrara un responsable
            instance.user_permissions = permisos.responsable_practicas()
        elif user.has_perm('registros.admin_vinc'): # Caso contrario es un administrador de vinculacion y registrara un responsable
            instance.user_permissions = permisos.responsable_vinculacion()
        return instance

    def estado(self, user, instance):
        if user.is_superuser: # Si es super usuario entonce registrara un administrador ya sea de practicas o vinculacion
            if self.cleaned_data.get('admin') == '1':
                for usuario in Permission.objects.get(codename='admin_prac').user_set.filter(is_active=True).exclude(id=instance.id):
                    usuario.is_active=False
                    usuario.save()
            elif self.cleaned_data.get('admin') == '2':
                for usuario in Permission.objects.get(codename='admin_vinc').user_set.filter(is_active=True).exclude(id=instance.id):
                    usuario.is_active=False
                    usuario.save()
        elif user.has_perm('registros.admin_prac'):
            for usuario in Permission.objects.get(codename='resp_prac').user_set.filter(is_active=True, perfil__carrera=instance.perfil.carrera).exclude(id=instance.id):
                usuario.is_active=False
                usuario.save()
        elif user.has_perm('registros.admin_vinc'):
            for usuario in Permission.objects.get(codename='resp_vinc').user_set.filter(is_active=True, perfil__carrera=instance.perfil.carrera).exclude(id=instance.id):
                usuario.is_active=False
                usuario.save()
        return instance

    def send_email(data):
        from django.core.mail import EmailMessage

        data = self.cleaned_data
        mensaje = u"""Bienvenido :
        username: {}
        clave {}""".format(data.get('username'), data.get('password1'))
        mail = EmailMessage('Instituto tecnologico Superior Sudamericano', mensaje, to=[data.get('email')])
        mail.send()