# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import forms_create
import forms_update

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.db import transaction
from ..registros.models import Estudiante
from ..modulos.reportes import reporte_practicas
from .models import Registro_practicas, Informe_practicas, Empresa

# Create your views here.
@login_required
@permission_required('practicas.add_registro_practicas')
@transaction.atomic
def crear(request):
    form = forms_create.RegistroForm(request.user, request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(request.user)
        return redirect('/')
    context = {
        'form': form,
        'title': 'REGISTRO PRACTICA'
    }
    return render(request, 'formularios/registro.html', context)

@login_required
@permission_required('practicas.add_informe_practicas')
@transaction.atomic
def crear_convenio(request):
    form = forms_create.ConvenioForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {
        'form': form,
        'title': 'CONVENIO'
    }
    return render(request, 'formulario.html', context)

@login_required
@permission_required('practicas.add_empresa')
@transaction.atomic
def crear_empresa(request):
    form = forms_create.EmpresaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(request.user)
        return redirect('/')
    context = {
        'form':form,
        'title':'NUEVA EMPRESA'
    }
    return render(request, 'formulario.html', context)

@login_required
@permission_required('practicas.change_registro_practicas')
@transaction.atomic
def proceso(request, pk):
    form = forms_update.RegistroForm(request.POST or None, request.FILES or None, instance=get_object_or_404(Registro_practicas, pk=pk, estado=True))
    if form.is_valid():
        form.save(request.user)
        return redirect('/')
    context = {
        'form':form,
        'title':'ENTREGA DE EVIDENCIAS'
    }
    return render(request, 'formulario.html', context)

@login_required
@permission_required('practicas.view_registro_practicas')
def tabla(request):
    data = None
    if request.user.has_perm('registros.admin_prac'):
        data = Registro_practicas.objects.filter(estado=True)
    elif request.user.has_perm('registros.resp_prac'):
        data = Registro_practicas.objects.filter(carrera=request.user.perfil.carrera, estado=True)
    context = {
        'practicas' : data,
        'title': 'ESTUDIANTES EN PROCESO'
    }
    return render(request, 'tablas/practicas.html', context)

@login_required
@permission_required('practicas.view_empresa')
def tabla_empresa(request):
    data = None
    if request.user.has_perm('registros.admin_prac'):
        data = Empresa.objects.all()
    elif request.user.has_perm('registros.resp_prac'):
        data = Empresa.objects.filter(carrera=request.user.perfil.carrera)
    context = {
        'empresas': data,
        'title': 'Empresas'
    }
    return render(request, 'tablas/empresas.html', context)

@login_required
@permission_required('practicas.reporte_convenio')
def reporte_convenio(request, pk):
    return reporte_practicas.convenio(pk)

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
    raise Http404