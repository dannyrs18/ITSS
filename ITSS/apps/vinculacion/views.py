# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import forms_create
import forms_update
import forms

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Proyecto_vinculacion, Componente, Actividad

# Create your views here.

@login_required
@permission_required('vinculacion.add_proyecto_vinculacion')
@transaction.atomic
def crear_proyecto(request):
    proyecto  = Proyecto_vinculacion()
    form = forms_create.ProyectoVinculacionForm(request.user, request.POST or None, request.FILES or None)
    formset = forms_create.ComponenteFormSet(request.POST or None, request.FILES or None, instance=proyecto)
    formset2 = forms_create.ComponenteFormSet2(request.POST or None, request.FILES or None, instance=proyecto, prefix='componente')
    if form.is_valid():
        proyecto = form.save(request.user)
        formset = forms_create.ComponenteFormSet(request.POST or None, request.FILES or None, instance=proyecto)
        if formset.is_valid() and formset2.is_valid():
            formset.save()
            messages.success(request, u'El proyecto se ha creado con exito!.')
            return redirect('/')
    if request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario.')
    context = {
        'form': form,
        'formset': formset,
        'formset2': formset2,
        'title': 'PROYECTO DE VINCULACIÓN'
    }
    return render(request, 'formularios/vinculacion_proyecto.html', context)

@login_required
@permission_required('vinculacion.add_componente')
@transaction.atomic
def crear_componente(request, slug):
    componente = get_object_or_404(Componente, slug=slug)
    actividad = Actividad()
    form = forms.ComponenteForm(componente, request.user, request.POST or None, request.FILES or None)
    form2 = forms_update.ComponenteForm(request.POST or None, request.FILES or None, instance=componente)
    formset = forms_create.ObjetivoFormSet(request.POST or None, request.FILES or None, instance=componente, prefix='objetivo')
    formset2 = forms_create.ActividadFormSet(request.POST or None, request.FILES or None, instance=componente, prefix='actividad')
    if form2.is_valid() and formset.is_valid():
        print 'ok'
        pass
    context = {
        'form': form,
        'form2': form2,
        'formset': formset,
        'formset2': formset2,
    }
    return render(request, 'formularios/vinculacion_componente.html', context)
        
@login_required
@permission_required('vinculacion.add_registro_vinculacion')
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
def evidencia(request):
    if request.is_ajax():
        evidencia = get_object_or_404(Estudiante, pk=request.POST.get('pk')).practicas.all()
        e = []
        for data in evidencia:
            e.append({
                'solicitud' : data.solicitud.url,
                'aceptacion' : data.aceptacion.url,
                'asistencia' : [i.evidencia.url for i in data.evidencia_asistencia.all()],
                'anexos' : [i.evidencia.url for i in data.evidencia_anexos.all()],
            })
        context = {
            'galeria' : e
        }
        return JsonResponse(context)
    return redirect('/')




########### pruebas
