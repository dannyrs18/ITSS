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
    form = forms_create.EmpresaForm(request.user, request.POST or None, request.FILES or None)
    #form2 = forms_create.EvidenciaEmpresaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        empresa = form.save(request.user)
        #form2.save(request.FILES.getlist('imagenes'), empresa)
        messages.success(request, u'El registro se creo exitosamente!.')
        return redirect('/')
    elif request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario.')
    context = {
        'form': form,
        #'form2': form2,
        'title': 'NUEVA EMPRESA'
    }
    return render(request, 'formulario.html', context)

@login_required
@permission_required('practicas.change_registro_practicas')
@transaction.atomic
def proceso(request, slug):
    practicas = get_object_or_404(Registro_practicas, slug=slug, estado=True)
    form = forms_update.RegistroForm(request.POST or None, request.FILES or None, instance=practicas)
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
@permission_required('practicas.change_empresa')
@transaction.atomic
def actualizar_empresa(request, slug):
    empresa = get_object_or_404(Empresa, slug=slug)
    form = forms_update.EmpresaForm(request.POST or None, request.FILES or None, instance=empresa)
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

def proceso_empresa(request, slug):
    empresa = get_object_or_404(Empresa, slug=slug)
    form = forms_update.EmpresaProcesoForm(request.POST or None, request.FILES or None, instance=empresa)
    form2 = forms_update.EvidenciaEmpresaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form2.save(request.FILES.getlist('imagenes'), empresa)
        messages.success(request, u'Se ha actualizado los datos exitosamente!.')
        return redirect('/')
    elif request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario..')
    context ={
        'form': form,
        'form2': form2,
    }
    return render(request, 'formularios/oficina.html', context)

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
    data = []
    if request.user.has_perm('registros.admin_prac'):
        data = Empresa.objects.filter(estado=True)
    elif request.user.has_perm('registros.resp_prac'):
        data = Empresa.objects.filter(carreras=request.user.perfil.carrera, estado=True)
    context = {
        'empresas': data,
        'title': 'EMPRESAS'
    }
    return render(request, 'tablas/empresas.html', context)

@login_required
@permission_required('practicas.view_empresa')
def tabla_empresa_proceso(request):
    data = []
    if request.user.has_perm('registros.admin_prac'):
        data = Empresa.objects.filter(estado=False)
    elif request.user.has_perm('registros.resp_prac'):
        for empresa in Empresa.objects.filter(carreras=request.user.perfil.carrera, estado=False):
            if empresa.carreras.count() == 1:
                data.append(empresa)
    context = {
        'empresas': data,
        'title': 'EMPRESAS'
    }
    return render(request, 'tablas/empresas_proceso.html', context)

@login_required
@permission_required('practicas.reporte_convenio_practicas')
def reporte_convenio(request, slug):
    try:
        convenio = reporte_practicas.convenio(slug)
        if not convenio:
            messages.error(request, u'Verifique si existe modelo de convenio.')
            return redirect('practicas:tabla_empresa_proceso')
    except:
        messages.error(request, u'Conflictos con el archivo base,')
    return convenio

@login_required
def evidencia_empresa(request):
    if request.is_ajax():
        empresa = get_object_or_404(Empresa, slug=request.POST.get('slug'))
        context = {
            'nombre' : empresa.nombre,
            'imagen' : [evidencia.imagen.url for evidencia in empresa.evidencias_empresa.all()],
        }
        return JsonResponse(context)
    raise Http404

@login_required
def evidencia_practicas(request):
    if request.is_ajax():
        practicas = get_object_or_404(Registro_practicas, id=request.POST.get('id'))
        context = {
            'nombre' : practicas.estudiante.get_full_name(),
            'imagen' : [evidencia.imagen.url for evidencia in practicas.evidencias_registro_practicas.all()],
        }
        return JsonResponse(context)
    raise Http404

@login_required
@permission_required('registros.reporte_estudiante')
def reporte_estudiante(request):
    form = forms.EstudianteForm(request.user, request.POST or None, request.FILES or None)
    if form.is_valid():
        response = reporte_practicas.estudiantes(form.cleaned_data.get('estudiante'))
        return response
    context = {
        'form' : form,
        'title' : 'REPORTE ESTUDIANTE'
    }
    return render(request, 'formulario.html', context)

@login_required
def reporte_empresas(request):
    empresas = Empresa.objects.none()
    if request.user.has_perm('registros.resp_prac'):
        empresas = Empresa.objects.filter(carrera = request.user.perfil.carrera)
    elif request.user.has_perm('registros.admin_prac'):
        empresas = Empresa.objects.filter()
    return reporte_practicas.empresas(empresas)

@login_required
def reporte_periodo(request):
    form = forms.PeriodoRegistroForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        from django.db.models import Q
        if request.user.has_perm('registros.admin_prac'):
            registro = Registro_practicas.objects.filter(Q(presentacion__gte=form.cleaned_data.get('inicio')) & Q(presentacion__lte=form.cleaned_data.get('fin')))
        elif request.user.has_perm('registros.resp_prac'):
            registro = Registro_practicas.objects.filter(Q(presentacion__gte=form.cleaned_data.get('inicio')) & Q(presentacion__lte=form.cleaned_data.get('fin')))
            registro = registro.filter(carrera=request.user.perfil.carrera)
        response = reporte_practicas.periodo(registro, form.cleaned_data)
        return response
    context = {
        'form': form,
        'title': 'REPORTE POR PERIODO'
    }
    return render(request, 'formulario.html', context)