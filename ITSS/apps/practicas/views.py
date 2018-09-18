# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.db import transaction
from .forms_create import ConvenioForm, EmpresaForm, RegistroForm
from ..registros.models import Estudiante

# Create your views here.
@login_required
@transaction.atomic
def crear(request):
    form = RegistroForm(request.user, request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(request.user)
        return redirect('/')
    context = {
        'form': form,
        'title': 'REGISTRO PRACTICA'
    }
    return render(request, 'formularios/registro.html', context)

@login_required
@transaction.atomic
def crear_convenio(request):
    form = ConvenioForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {
        'form': form,
        'title': 'CONVENIO'
    }
    return render(request, 'formulario.html', context)

@login_required
@transaction.atomic
def crear_empresa(request):
    form = EmpresaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(request.user)
        return redirect('/')
    context = {
        'title':'NUEVA EMPRESA',
        'form':form
    }
    return render(request, 'formulario.html', context)

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