# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .forms_create import ConvenioForm, EntidadForm

# Create your views here.

@login_required
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

@login_required
def crear_entidad(request):
    form = EntidadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        model = form.save(commit=False)
        if request.user.perfil.respVinculacion:
            model.carreras.add(request.user.perfil.carrera)
        model.save()
        return redirect('/')
    context = {
        'title':'NUEVA ENTIDAD',
        'form':form
    }
    return render(request, 'formulario.html', context)