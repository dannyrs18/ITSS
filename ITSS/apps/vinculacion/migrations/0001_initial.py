# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-18 21:30
from __future__ import unicode_literals

import apps.modulos.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registros', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos', verbose_name='Logo')),
                ('telefono', models.CharField(max_length=15, verbose_name='Telefono')),
                ('inicio', models.DateField(verbose_name='Inicio del Convenio')),
                ('fin', models.DateField(verbose_name='Finalizacion del Convenio')),
                ('correo', models.EmailField(max_length=254, verbose_name='Correo')),
                ('direccion', models.TextField(verbose_name='Direccion')),
                ('estado', models.BooleanField(default=False, verbose_name='Estado')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('gerente', models.CharField(max_length=100, verbose_name='Gerente')),
                ('descripcion', models.TextField(verbose_name='Descripci\xf3n')),
                ('carreras', models.ManyToManyField(related_name='entidades', to='registros.Carrera')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('view_entidad', 'Puede acceder a Entidad')],
            },
        ),
        migrations.CreateModel(
            name='Informe_vinculacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('convenio', models.FileField(upload_to='informes_vinculacion', validators=[apps.modulos.validators.valid_extension], verbose_name='Convenio')),
            ],
            options={
                'permissions': [('view_informe_vinculacion', 'Puede acceder a Informe Vinculacion')],
            },
        ),
    ]
