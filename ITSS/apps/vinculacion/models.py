# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from ..registros.models import Oficina, Carrera, Perfil
from ..modulos.validators import valid_extension

class Entidad(Oficina):
    responsable = models.CharField(_('Responsable'), max_length=100)
    cargo = models.CharField(_('Cargo'), max_length=100)
    descripcion = models.TextField(_('Descripción'))
    carreras = models.ManyToManyField(Carrera, related_name='entidades')
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ('view_entidad', 'Puede acceder a Entidad'),
        ]

    def __unicode__(self):
        return self.nombre

class Informe_vinculacion(models.Model):
    convenio = models.FileField(_('Convenio'), upload_to='informes_vinculacion', validators=[valid_extension])

    class Meta:
        permissions = [
            ('view_informe_vinculacion', 'Puede acceder a Informe Vinculacion'),
        ]

    def __unicode__(self):
        return self.convenio