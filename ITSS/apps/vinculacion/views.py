# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import forms_create
import forms_update
import forms

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.db import transaction
from ..modulos.reportes import reporte_vinculacion
from ..registros.models import Estudiante
from .models import Proyecto_vinculacion, Componente, Actividad, Entidad, Proyecto_vinculacion

# Create your views here.

@login_required
@permission_required('vinculacion.add_proyecto_vinculacion')
@transaction.atomic
def crear_proyecto(request):
    proyecto  = Proyecto_vinculacion()
    form = forms_create.ProyectoVinculacionForm(request.user, request.POST or None, request.FILES or None)
    formset = forms_create.ComponenteFormSet(request.POST or None, request.FILES or None, instance=proyecto)
    if form.is_valid() and formset.is_valid():
        proyecto = form.save(request.user)
        formset = forms_create.ComponenteFormSet(request.POST or None, request.FILES or None, instance=proyecto)
        if formset.is_valid():
            formset.save()
            messages.success(request, u'El proyecto se ha creado con exito!.')
            return redirect('/')
    if request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario.')
    context = {
        'form': form,
        'formset' : formset,
        'title': 'PROYECTO DE VINCULACIÓN'
    }
    return render(request, 'formularios/vinculacion_proyecto.html', context)

@login_required
@permission_required('vinculacion.add_componente')
@transaction.atomic
def crear_componente(request, slug):
    componente = get_object_or_404(Componente, slug=slug, estado=1)
    form = forms.ComponenteForm(componente, request.user, request.POST or None, request.FILES or None)
    form2 = forms_update.ComponenteForm(request.POST or None, request.FILES or None, instance=componente)
    formset = forms_create.ObjetivoFormSet(request.POST or None, request.FILES or None, instance=componente, prefix='objetivo')
    formset2 = forms_create.ActividadFormSet(request.POST or None, request.FILES or None, instance=componente, prefix='actividad')
    formset3 = forms_create.RecursoHumanoFormSet(request.POST or None, request.FILES or None, instance=componente, prefix='recurso_humano')
    formset4 = forms_create.RecursoFinancieroFormSet(request.POST or None, request.FILES or None, instance=componente, prefix='recurso_financiero')
    formset5 = forms_create.RecursoMaterialFormSet(request.POST or None, request.FILES or None, instance=componente, prefix='recurso_material')
    formset6 = forms_create.RecursoTecnologicoFormSet(request.POST or None, request.FILES or None, instance=componente, prefix='recurso_tecnologico')
    formset7 = forms_create.EvaluacionFormset(request.POST or None, request.FILES or None, form_kwargs={'componente':componente}, instance=componente, prefix='evaluacion')
    if form2.is_valid() and formset.is_valid() and formset2.is_valid() and formset3.is_valid() and formset4.is_valid() and formset5.is_valid() and formset6.is_valid() and formset7.is_valid():
        form2.save(request.user)
        formset.save()
        formset2.save()
        formset3.save()
        formset4.save()
        formset5.save()
        formset6.save()
        formset7.save()
        messages.success(request, u'Se ha completado exitosamente!.')
        return redirect('index')
    elif request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario.')
    context = {
        'form': form,
        'form2': form2,
        'formset': formset,
        'formset2': formset2,
        'formset3': formset3,
        'formset4': formset4,
        'formset5': formset5,
        'formset6': formset6,
        'formset7': formset7,
        'title': 'COMPONENTE'
    }
    return render(request, 'formularios/vinculacion_componente.html', context)


@login_required
@permission_required('vinculacion.add_actividad_vinculacion')
@transaction.atomic
def crear_actividad(request):
    pass

@login_required
@permission_required('vinculacion.add_informe_vinculacion')
@transaction.atomic
def crear_convenio(request):
    form = forms_create.ConvenioForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, u'El convenio se creo exitosamente!.')
        return redirect('/')
    elif request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario.')
    context = {
        'form': form,
        'title': 'CONVENIO'
    }
    return render(request, 'formulario.html', context)

@login_required
@permission_required('vinculacion.add_entidad')
@transaction.atomic
def crear_entidad(request):
    form = forms_create.EntidadForm(request.user, request.POST or None, request.FILES or None)
    form2 = forms_create.EvidenciaEntidadForm(request.POST or None, request.FILES or None)
    if form.is_valid() and form2.is_valid():
        entidad = form.save(request.user)
        form2.save(request.FILES.getlist('imagenes'), entidad)
        messages.success(request, u'El registro se creo exitosamente!.')
        return redirect('/')
    elif request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario.')
    context = {
        'title':'NUEVA ENTIDAD',
        'form':form,
        'form2': form2
    }
    return render(request, 'formularios/oficina.html', context)

@login_required
@permission_required('vinculacion.change_entidad')
@transaction.atomic
def actualizar_entidad(request, slug):
    entidad = get_object_or_404(Entidad, slug=slug)
    form = forms_update.EntidadForm(request.POST or None, request.FILES or None, instance=entidad)
    if form.is_valid():
        form.save()
        messages.success(request, u'Se ha actualizado los datos exitosamente!.')
        return redirect('/')
    elif request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario..')
    context ={
        'form': form
    }
    return render(request, 'formulario.html', context)

@login_required
@permission_required('vinculacion.view_proyecto_vinculacion')
def tabla_proceso(request):
    if request.user.has_perm('registros.admin_vinc'):
        proyectos = Proyecto_vinculacion.objects.filter(estado=True)
    elif request.user.has_perm('registros.resp_vinc'):
        proyectos = Proyecto_vinculacion.objects.filter(estado=True, carrera=request.user.perfil.carrera)
    context = {
        'proyectos' : proyectos
    }
    return render(request, 'tablas/vinculacion_proceso.html', context)

@login_required
@permission_required('vinculacion.view_entidad')
def tabla_entidad(request):
    if request.user.has_perm('registros.admin_vinc'):
        entidades = Entidad.objects.all()
    elif request.user.has_perm('registros.resp_vinc'):
        entidades = Entidad.objects.filter(carreras=request.user.perfil.carrera)
    context = {
        'entidades' : entidades
    }
    return render(request, 'tablas/entidades.html', context)

@login_required
@permission_required('vinculacion.reporte_convenio_vinculacion')
def reporte_convenio(request, slug):
    convenio = reporte_vinculacion.convenio(slug)
    if not convenio:
        messages.error(request, u'Verifique si existe modelo de convenio.')
        return redirect('vinculacion:tabla_entidad')
    return convenio

@login_required
@permission_required('registros.reporte_estudiante')
def reporte_estudiante(request):
    form = forms.EstudianteForm(request.user, request.POST or None, request.FILES or None)
    if form.is_valid():
        response = reporte_vinculacion.estudiantes(form.cleaned_data.get('estudiante'))
        return response
    context = {
        'form': form
    }
    return render(request, 'formulario.html', context)

@login_required
@permission_required('vinculacion.reporte_entidad')
def reporte_entidades(request):
    entidades = Entidad.objects.all()
    response = reporte_vinculacion.entidades(entidades)
    return response

@login_required
def reporte_periodo(request):
    form = forms.PeriodoRegistroForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        pass
    context = {
        'form': form,
        'title': 'REPORTE POR PERIODO'
    }
    return render(request, 'formulario.html', context)

@login_required
def ajax_evidencia_entidad(request):
    if request.is_ajax():
        entidad = get_object_or_404(Entidad, slug=request.POST.get('slug'))
        context = {
            'nombre' : entidad.nombre,
            'imagen' : [evidencia.imagen.url for evidencia in entidad.evidencias_entidad.all()],
        }
        return JsonResponse(context)
    raise Http404