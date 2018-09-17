# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Permission

class RootForm(UserCreationForm):

    PRACTICAS, VINCULACION = 1, 2
    SELECT = (
        (None, '-----'),
        (PRACTICAS,_(u'PRACTICAS')),
        (VINCULACION, _(u'VINCULACIÓN')),
    )

    username = forms.CharField(max_length='20', label=_('Usuario'))
    avatar = forms.ImageField(label=_('Imagen de perfil'), required=False)
    cedula = forms.IntegerField(label=_('Cedula'))
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
        self.fields['avatar'].widget.attrs.update({'class' : 'form-control'})
        self.fields['admin'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password1'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password2'].widget.attrs.update({'class' : 'form-control'})

    def save(self, user, commit=True):
        instance = super(RootForm, self).save(commit=True)
        if user.is_superuser:
            perm_add = Permission.objects.get(codename='add_user')
            perm_change = Permission.objects.get(codename='change_user')
            if self.cleaned_data.get('admin') == '1':
                perm_admin = Permission.objects.get(codename='admin_prac')
                instance.user_permissions = [perm_add, perm_change, perm_admin]
            else:
                perm_admin = Permission.objects.get(codename='admin_vinc')
                instance.user_permissions = [perm_add, perm_change, perm_admin]
        if commit:
            instance.save()
            instance.refresh_from_db()  # cargar la instancia de perfil creada por la señal
            instance.perfil.avatar = self.cleaned_data.get('avatar')
            instance.perfil.cedula = self.cleaned_data.get('cedula')
            instance.save()
        return instance