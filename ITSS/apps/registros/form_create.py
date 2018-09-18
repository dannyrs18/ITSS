# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Permission
from .models import Docente, Carrera

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
    telefono = forms.IntegerField(label=_('Telefono'))
    avatar = forms.ImageField(label=_('Imagen de perfil'), required=False)

    class Meta:
        model = User
        fields = ('admin', 'carrera', 'docente', 'first_name', 'last_name', 'cedula', 'telefono', 'email', 'avatar', 'username', 'password1', 'password2')

    def __init__(self, user, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class' : 'form-control'})
        self.fields['carrera'].widget.attrs.update({'class' : 'form-control js-example-basic-single'})
        self.fields['docente'].widget.attrs.update({'class' : 'form-control js-example-basic-single'})
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        self.fields['cedula'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        self.fields['telefono'].widget.attrs.update({'class' : 'form-control', 'readonly':'readonly'})
        if not user.is_superuser:
            del self.fields['admin']
        else:
            del self.fields['carrera']

    def save(self, user, commit=True):
        instance = super(UserForm, self).save(commit=True)
        self.permisos(user, instance)
        if self.cleaned_data.get('carrera', ''):
            instance.perfil.carrera = self.cleaned_data.get('carrera', '')
        if commit:
            instance.refresh_from_db()  # cargar la instancia de perfil creada por la señal
            instance.perfil.docente = self.cleaned_data.get('docente', '')
            instance.perfil.avatar = self.cleaned_data.get('avatar')
            instance.save()
        return instance

    def permisos(self, user, instance):
        if user.is_superuser:
            perm_add = Permission.objects.get(codename='add_user')
            if self.cleaned_data.get('admin') == '1':
                perm_inf2 = Permission.objects.get(codename='add_informe_practicas')
                perm_emp = Permission.objects.get(codename='view_empresa')
                perm_emp_add = Permission.objects.get(codename='add_empresa')
                perm_admin = Permission.objects.get(codename='admin_prac')
                instance.user_permissions = [perm_admin, perm_add, perm_inf2, perm_emp, perm_emp_add]
            elif self.cleaned_data.get('admin') == '2':
                perm_inf2 = Permission.objects.get(codename='add_informe_vinculacion')
                perm_admin = Permission.objects.get(codename='admin_vinc')
                perm_ent = Permission.objects.get(codename='view_entidad')
                perm_ent_add = Permission.objects.get(codename='add_entidad')
                instance.user_permissions = [perm_admin, perm_add, perm_inf2, perm_ent, perm_ent_add]
        elif user.has_perm('registros.admin_prac'):
            perm_resp = Permission.objects.get(codename='resp_prac')
            instance.user_permissions = [perm_resp,]
        elif user.has_perm('registros.admin_vinc'):
            perm_resp = Permission.objects.get(codename='resp_vinc')
            instance.user_permissions = [perm_resp,]