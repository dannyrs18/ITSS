# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-16 17:33
from __future__ import unicode_literals

import apps.modulos.validators
import apps.vinculacion.models
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
            name='Actividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre de la Actividad')),
                ('realizado', models.TextField(verbose_name='Realizado')),
                ('meta', models.TextField(verbose_name='Meta')),
                ('resultado', models.TextField(verbose_name='Resultado')),
                ('cumplimiento', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='% de Cumplimiento')),
            ],
        ),
        migrations.CreateModel(
            name='Actividad_Ac',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Actividades')),
            ],
        ),
        migrations.CreateModel(
            name='Actividad_vinculacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300, verbose_name='Nombre de la Actividad')),
                ('inicio', models.DateField(verbose_name='Fecha de inicio')),
                ('fin', models.DateField(verbose_name='Fecha de culminaci\xf3n')),
                ('slug', models.SlugField(blank=True)),
                ('descripcion', models.TextField(verbose_name='Descripci\xf3n')),
                ('justificacion', models.TextField(verbose_name='Justificaci\xf3n')),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividades_vinculacion', to='registros.Carrera')),
            ],
            options={
                'permissions': [('view_actividad_vinculacion', 'Puede acceder a Actividades de vinculacion')],
            },
        ),
        migrations.CreateModel(
            name='Componente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre del Componente')),
                ('introduccion', models.TextField(blank=True, null=True, verbose_name='Introduccion')),
                ('observacion', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('inicio', models.DateField(blank=True, null=True, verbose_name='Fecha de inicio')),
                ('fin', models.DateField(blank=True, null=True, verbose_name='Fecha de finalizaci\xf3n')),
                ('estado', models.PositiveSmallIntegerField(default=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)])),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entidad',
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
                ('encargado', models.CharField(max_length=100, verbose_name='Responsable')),
                ('cargo', models.CharField(max_length=100, verbose_name='Cargo')),
                ('fax', models.CharField(blank=True, max_length=20, null=True, verbose_name='Fax')),
                ('descripcion', models.TextField(verbose_name='Descripci\xf3n')),
                ('carreras', models.ManyToManyField(related_name='entidades', to='registros.Carrera')),
                ('responsable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('view_entidad', 'Puede acceder a Entidad'), ('reporte_entidad', 'Puede acceder a reporte de Entidad')],
            },
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('hora_entrada', models.TimeField()),
                ('hora_salida', models.TimeField()),
                ('total_horas', models.PositiveSmallIntegerField()),
                ('puntualidad', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='Puntualidad (1)')),
                ('asistencia', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='Asistencia (1)')),
                ('actitud', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)], verbose_name='Actitud frente a actividades (2)')),
                ('cumplimiento', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)], verbose_name='Cumplimiento, Objetivos (2)')),
                ('aplicacion', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)], verbose_name='Aplicacion de habilidades y destreza (2)')),
                ('satisfaccion', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)], verbose_name='Nivel de satisfaccion (2)')),
                ('promedio', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Promedio')),
                ('actividad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='vinculacion.Actividad_vinculacion')),
                ('componente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='vinculacion.Componente')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='registros.Estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='Evidencia_actividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(max_length=200, upload_to=apps.vinculacion.models.generate_evidencia_actividad)),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidencias_actividades', to='vinculacion.Actividad_vinculacion')),
            ],
        ),
        migrations.CreateModel(
            name='Evidencia_proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(max_length=200, upload_to=apps.vinculacion.models.generate_evidencia_proyecto)),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidencias_proyecto', to='vinculacion.Componente')),
            ],
        ),
        migrations.CreateModel(
            name='Evidencias_Entidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to=apps.vinculacion.models.generate_evidencia_entidad, verbose_name='Evidencias Fotograficas')),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidencias_entidad', to='vinculacion.Entidad')),
            ],
        ),
        migrations.CreateModel(
            name='Informe_vinculacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('convenio', models.FileField(upload_to='informes_vinculacion', verbose_name='Convenio')),
            ],
            options={
                'permissions': [('view_informe_vinculacion', 'Puede acceder a Informe Vinculacion'), ('reporte_convenio_vinculacion', 'Puede realizar el reporte de convenio')],
            },
        ),
        migrations.CreateModel(
            name='Objetivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objectivos', to='vinculacion.Componente')),
            ],
        ),
        migrations.CreateModel(
            name='Objetivo_Especifico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Objetivos Especificos')),
                ('actividad_vinculacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objetivos_especificos', to='vinculacion.Actividad_vinculacion')),
            ],
        ),
        migrations.CreateModel(
            name='Objetivo_General',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Objetivos Generales')),
                ('actividad_vinculacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objetivos_generales', to='vinculacion.Actividad_vinculacion')),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto_vinculacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300, verbose_name='Nombre del Proyecto')),
                ('estado', models.BooleanField(default=True)),
                ('inicio', models.DateField(auto_now_add=True)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyectos_vinculacion', to='registros.Carrera')),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyectos_vinculacion', to='vinculacion.Entidad')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyectos_vinculacion', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('view_proyecto_vinculacion', 'Puede acceder a Registro Vinculacion'), ('reporte_registro_proyectos', 'Puede acceder a reportes de Proyecto')],
            },
        ),
        migrations.CreateModel(
            name='Recurso_financiero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Cantidad')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre del Recurso')),
                ('descripcion', models.TextField(verbose_name='Descripcion')),
                ('unitario', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Valor Unitario')),
                ('total', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Valor Total')),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recursos_financieros', to='vinculacion.Componente')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recurso_humano',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Cantidad')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre del Recurso')),
                ('descripcion', models.TextField(verbose_name='Descripcion')),
                ('unitario', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Valor Unitario')),
                ('total', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Valor Total')),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recursos_humanos', to='vinculacion.Componente')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recurso_material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Cantidad')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre del Recurso')),
                ('descripcion', models.TextField(verbose_name='Descripcion')),
                ('unitario', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Valor Unitario')),
                ('total', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Valor Total')),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recursos_materiales', to='vinculacion.Componente')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recurso_tecnologico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Cantidad')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre del Recurso')),
                ('descripcion', models.TextField(verbose_name='Descripcion')),
                ('unitario', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Valor Unitario')),
                ('total', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Valor Total')),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recursos_tecnologicos', to='vinculacion.Componente')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='componente',
            name='proyecto_vinculacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='componentes', to='vinculacion.Proyecto_vinculacion'),
        ),
        migrations.AddField(
            model_name='componente',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='componentes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='componente',
            name='seccion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='componentes', to='registros.Seccion'),
        ),
        migrations.AddField(
            model_name='actividad_vinculacion',
            name='entidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividades_vinculacion', to='vinculacion.Entidad'),
        ),
        migrations.AddField(
            model_name='actividad_vinculacion',
            name='responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividades_vinculacion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='actividad_ac',
            name='actividad_vinculacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividades_ac', to='vinculacion.Actividad_vinculacion'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='componente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividades', to='vinculacion.Componente'),
        ),
    ]
