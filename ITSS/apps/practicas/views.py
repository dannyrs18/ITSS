# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import forms_create
import forms_update

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.contrib import messages
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
    form2 = forms_create.EvidenciaRegistroForm(request.POST or None, request.FILES or None)
    if form.is_valid() and form2.is_valid():
        registro = form.save(request.user)
        form2.save(request.FILES.getlist('imagenes'), registro)
        messages.success(request, u'El registro se creo exitosamente!.')
        return redirect('/')
    elif request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario.')
    context = {
        'form': form,
        'form2': form2,
        'title': 'REGISTRO PRACTICA'
    }
    return render(request, 'formularios/practicas.html', context)

@login_required
@permission_required('practicas.add_informe_practicas')
@transaction.atomic
def crear_convenio(request):
    form = forms_create.ConvenioForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, u'El registro se creo exitosamente!.')
        return redirect('/')
    elif request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario.')
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
    form2 = forms_create.EvidenciaEmpresaForm(request.POST or None, request.FILES or None)
    if form.is_valid() and form2.is_valid():
        empresa = form.save(request.user)
        form2.save(request.FILES.getlist('imagenes'), empresa)
        messages.success(request, u'El registro se creo exitosamente!.')
        return redirect('/')
    elif request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario.')
    context = {
        'form': form,
        'form2': form2,
        'title': 'NUEVA EMPRESA'
    }
    return render(request, 'formularios/empresa.html', context)

@login_required
@permission_required('practicas.change_registro_practicas')
@transaction.atomic
def proceso(request, slug):
    form = forms_update.RegistroForm(request.POST or None, request.FILES or None, instance=get_object_or_404(Registro_practicas, slug=slug, estado=True))
    form2 = forms_create.EvidenciaRegistroForm(request.POST or None, request.FILES or None)
    if form.is_valid() and form2.is_valid():
        registro = form.save(request.user)
        form2.save(request.FILES.getlist('imagenes'), registro)
        messages.success(request, u'El proceso ha concluido exitosamente!.')
        return redirect('/')
    elif request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario.')
    context = {
        'form': form,
        'form2': form2,
        'title':'ENTREGA DE EVIDENCIAS'
    }
    return render(request, 'formularios/practicas.html', context)

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
        data = Empresa.objects.filter(carreras=request.user.perfil.carrera)
    context = {
        'empresas': data,
        'title': 'EMPRESAS'
    }
    return render(request, 'tablas/oficina.html', context)

@login_required
@permission_required('practicas.reporte_convenio_practicas')
def reporte_convenio(request, slug):
    return reporte_practicas.convenio(slug)

@login_required
def evidencia_empresa(request):
    if request.is_ajax():
        empresa = get_object_or_404(Empresa, slug=request.POST.get('slug'))
        data = []
        context = {
            'nombre' : empresa.nombre,
            'imagen' : [evidencia.imagen.url for evidencia in empresa.evidencias_empresa.all()],
        }
        return JsonResponse(context)
    raise Http404