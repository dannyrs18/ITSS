# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.db import transaction
from .form_create import UserForm
from ..modulos import web_services as _
from .models import Estudiante, Docente, Carrera

@login_required
@permission_required('auth.add_user') #raise_exception=True
@transaction.atomic
def crear_usuario(request):
    form = UserForm(request.user, request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(request.user)
        return redirect('index')
    context = {
        'form': form,
        'title': 'CREAR USUARIO'
    }
    return render(request, 'formularios/usuario.html', context)

# Web Services
@login_required
@user_passes_test(lambda u: u.is_superuser)
def tabla_registros(request):
    context = {
        'estudiantes': Estudiante.objects.all(),
        'docentes' : Docente.objects.all(),
        'carreras' : Carrera.objects.all(),
    }
    return render(request, 'tablas/web_services.html', context)

@login_required
def tabla_estudiantes(request):
    estudiantes = None
    if request.user.has_perms(['registros.admin_prac','registros.admin_vinc']):
        estudiantes = Estudiante.objects.all()
    elif request.user.has_perms(['registros.resp_prac','registros.resp_vinc']):
        estudiantes = Estudiante.objects.filter(carrera=request.user.perfil.carrera)
    context = {
        'estudiantes':estudiantes,
        'title': 'ESTUDIANTES'
    }
    return render(request, 'tablas/estudiantes.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def web_services(request):
    try:
        carreras()
        estudiantes()
        docentes()
    except :
        pass
    return redirect('registro:tabla_web_services')

def carreras():
    carreras = _.get_data(_._carreras)
    for carrera in carreras:
        if not Carrera.objects.filter(codigo=carrera['codigo']).exists():
            instance = Carrera()
            instance.codigo = carrera['codigo']
            instance.nombre = carrera['nombre']
            instance.save()
            actualizacion = True

def estudiantes():
    carreras = Carrera.objects.all()
    for carrera in carreras:
        estudiantes = _.get_data(_._listadoEstudiantesCarrera, carrera.codigo)
        for estudiante in estudiantes:
            if not Estudiante.objects.filter(cedula=estudiante['cedula']).exists():
                instance = Estudiante()
                instance.nombres = estudiante['nombres']
                instance.apellidos = estudiante['apellidos']
                instance.cedula = estudiante['cedula']
                instance.genero = estudiante['genero']
                instance.ciclo = estudiante['ciclo']
                instance.carrera = get_object_or_404(Carrera,nombre = estudiante['carrera'])
                instance.save()

def docentes():
    docentes = _.get_data(_._listadoDocentesPeriodoActual)
    for docente in docentes:
        if not Docentes.objects.filter(cedula=docente['cedula']).exists():
            instance = Docentes()
            instance.nombres = docente['nombres']
            instance.apellidos = docente['apellidos']
            instance.cedula = docente['cedula']
            instance.telefono = docente['telefono']
            instance.save()

@login_required
def ajax_docente(request):
    if request.is_ajax():
        docente = Docente.objects.get(pk=request.POST.get('pk'))
        data = {
            'nombres': docente.nombres,
            'apellidos': docente.apellidos,
            'cedula': docente.cedula,
            'telefono': docente.telefono
        }
        return JsonResponse(data)
    raise Http404

@login_required
def ajax_estudiante(request):
    if request.is_ajax():
        estudiante = Estudiante.objects.get(pk=request.POST.get('pk'))
        data = {
            'nombres': estudiante.nombres,
            'apellidos': estudiante.apellidos,
            'cedula': estudiante.cedula,
        }
        return JsonResponse(data)
    raise Http404