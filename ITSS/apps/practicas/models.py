# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..registros.models import Oficina, Carrera

class Empresa(Oficina): # PRACTICAS
    departamento = models.CharField(max_length=100)
    responsable = models.CharField(max_length=100)
    carreras = models.ManyToManyField(Carrera, related_name='empresas')

    def __unicode__(self):
        return self.nombre