# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-01 05:39
from __future__ import unicode_literals

import apps.modulos.validators
import apps.practicas.models
from django.conf import settings
import django.core.validators
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
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos', validators=[apps.modulos.validators.valid_extension], verbose_name='Logo de la Empresa')),
                ('telefono', models.CharField(max_length=15, verbose_name='Tel\xe9fono')),
                ('inicio', models.DateField(verbose_name='Inicio del Convenio')),
                ('fin', models.DateField(verbose_name='Finalizacion del Convenio')),
                ('correo', models.EmailField(max_length=254, verbose_name='Correo')),
                ('direccion', models.TextField(verbose_name='Direcci\xf3n')),
                ('estado', models.BooleanField(default=False, verbose_name='Estado')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True)),
                ('gerente', models.CharField(max_length=100, verbose_name='Nombre del Gerente')),
                ('descripcion', models.TextField(verbose_name='Descripci\xf3n')),
                ('carreras', models.ManyToManyField(related_name='empresas', to='registros.Carrera')),
                ('responsable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('view_empresa', 'Puede acceder a Empresa'), ('reporte_empresa', 'Puede acceder a reporte de Empresa')],
            },
        ),
        migrations.CreateModel(
            name='Evidencias_Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to=apps.practicas.models.generate_evidencia_empresa, verbose_name='Evidencias Fotograficas')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidencias_empresa', to='practicas.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Evidencias_registro_practicas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to=apps.practicas.models.generate_registro_practicas, verbose_name='Evidencias Fotograficas')),
            ],
        ),
        migrations.CreateModel(
            name='Informe_practicas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('convenio', models.FileField(upload_to='informes_practicas', validators=[apps.modulos.validators.valid_extension])),
            ],
            options={
                'permissions': [('view_informe_practicas', 'Puede acceder a Informe Practicas'), ('reporte_convenio_practicas', 'Puede realizar el reporte de convenio')],
            },
        ),
        migrations.CreateModel(
            name='Registro_practicas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presentacion', models.DateField(verbose_name='Fecha de Presentacion')),
                ('fin', models.DateField(blank=True, null=True, verbose_name='Fecha de finalizaci\xf3n')),
                ('horas', models.PositiveIntegerField(default=0, verbose_name='Horas completadas')),
                ('calificacion', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Calificaci\xf3n del Estudiante')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado del registro')),
                ('slug', models.SlugField(blank=True)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros_practicas', to='registros.Carrera')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros_practicas', to='practicas.Empresa')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros_practicas', to='registros.Estudiante')),
            ],
            options={
                'permissions': (('view_registro_practicas', 'Puede visualizar el Registro'), ('reporte_registro_practicas', 'Puede acceder a reportes de Registro')),
            },
        ),
        migrations.AddField(
            model_name='evidencias_registro_practicas',
            name='registro_practicas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidencias_registro_practicas', to='practicas.Registro_practicas'),
        ),
    ]
