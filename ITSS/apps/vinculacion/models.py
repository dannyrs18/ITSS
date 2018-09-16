# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..registros.models import Oficina, Carrera

class Entidad(Oficina):
    gerente = models.CharField(max_length=100)
    descripcion = models.TextField()
    carreras = models.ManyToManyField(Carrera, related_name='entidades') # vinculacion puede tener una o varias

    def __unicode__(self):
        return self.nombre