# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-05 02:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vinculacion', '0002_auto_20190104_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entidad',
            name='inicio',
            field=models.DateField(null=True, verbose_name='Inicio del Convenio'),
        ),
    ]
