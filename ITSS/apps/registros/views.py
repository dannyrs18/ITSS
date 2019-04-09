# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404, FileResponse
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from .forms_create import UserForm, CoordinadorForm
from .forms_update import PasswordForm, UserPerfilForm
from ..modulos import web_services as _, cron_jobs
from ..modulos.reportes import reporte_practicas
from .models import Estudiante, Docente, Carrera, Seccion, Perfil, Coordinador
from ..vinculacion.models import Entidad
from ..practicas.models import Empresa
from django.contrib.auth.models import Permission
from .forms import ErrorForm

from django.contrib.auth.forms import PasswordChangeForm

@login_required
@permission_required('auth.add_user') #raise_exception=True
@transaction.atomic
def crear_usuario(request):
    form = UserForm(request.user, request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, u'El usuario se ha creado exitosamente!.')
        return redirect('index')
    elif request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario')
    context = {
        'form': form,
        'title': 'CREAR USUARIO'
    }
    return render(request, 'formularios/usuario.html', context)



@login_required
@permission_required('registros:add_coordinador') #raise_exception=True
@transaction.atomic
def crear_coordinador(request):
    form = CoordinadorForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, u'El coordinador se ha creado exitosamente!.')
        return redirect('index')
    elif request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario')
    context = {
        'form': form
    }
    return render(request, 'formulario.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def modificar_usuario(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    form = UserPerfilForm(request.POST or None, request.FILES or None, instance=perfil)
    if form.is_valid():
        form.save()
        messages.success(request, u'El usuario se ha modificado exitosamente!.')
        return redirect('index')
    if request.POST:
        messages.error(request, u'Valores ingresados incorrectos dentro del formulario')
    context = {
        'form': form,
        'title': 'MODIFICAR DATOS'
    }
    return render(request, 'formularios/usuario.html', context)


@login_required
@permission_required('auth.change_user') 
@transaction.atomic
def modificar_clave(request):
    form = PasswordForm(request.user, request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'La clave ha sido actualizada exitosamentes')
        return redirect('index')
    elif request.POST:
        messages.error(request, 'Valores ingresados incorrectos')
    context = {
        'form': form
    }
    return render(request, 'formulario.html', context)


@login_required
@permission_required('auth.change_user') 
@transaction.atomic
def modificar_estado(request, slug):
    usuario = get_object_or_404(Perfil, slug=slug).user
    if usuario.is_active:
        usuario.is_active=False
        usuario.save()
        messages.success(request, 'Se ha dado al usuario {} de baja!.'.format(usuario.get_full_name()))
    else:
        if Permission.objects.get(codename='admin_prac').user_set.filter(id=usuario.id).exists():
            for value in Permission.objects.get(codename='admin_prac').user_set.filter(is_active=True):
                value.is_active=False
                value.save()
        elif Permission.objects.get(codename='admin_vinc').user_set.filter(id=usuario.id).exists():
            for value in Permission.objects.get(codename='admin_vinc').user_set.filter(is_active=True):
                value.is_active=False
                value.save()
        elif Permission.objects.get(codename='resp_prac').user_set.filter(id=usuario.id).exists():
            for value in Permission.objects.get(codename='resp_prac').user_set.filter(perfil__carrera=usuario.perfil.carrera).exclude(id=usuario.id):
                value.is_active=False
                value.save()
        elif Permission.objects.get(codename='resp_vinc').user_set.filter(id=usuario.id).exists():
            for value in Permission.objects.get(codename='resp_vinc').user_set.filter(perfil__carrera=usuario.perfil.carrera).exclude(id=usuario.id):
                value.is_active=False
                value.save()
        usuario.is_active=True
        usuario.save()
        messages.success(request, 'Se ha activado la cuenta de {} exitosamente'.format(usuario.get_full_name()))
    return redirect('registro:tabla_usuarios')

# Web Services
@login_required
@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def tabla_registros(request):
    context = {
        'estudiantes': Estudiante.objects.all(),
        'docentes' : Docente.objects.all(),
        'carreras' : Carrera.objects.all(),
        'secciones' : Seccion.objects.all()
    }
    return render(request, 'tablas/web_services.html', context)

@login_required
@permission_required('registros.view_perfil')
def tabla_usuarios(request):
    from django.contrib.auth.models import User, Permission
    from django.db.models import Q
    usuarios = []
    if request.user.is_superuser:        
        usuarios = User.objects.filter(Q(user_permissions=Permission.objects.get(codename='admin_prac'))|Q(user_permissions=Permission.objects.get(codename='admin_vinc'))).distinct()
    elif request.user.has_perm('registros.admin_prac'):
        usuarios = User.objects.filter(Q(user_permissions=Permission.objects.get(codename='resp_prac'))).distinct()
    elif request.user.has_perm('registros.admin_vinc'):
        usuarios = User.objects.filter(Q(user_permissions=Permission.objects.get(codename='resp_vinc'))).distinct()
    context = {
        'usuarios': usuarios
    }
    return render(request, 'tablas/usuarios.html', context)
    
@login_required
@permission_required('registros.view_estudiante')
def tabla_estudiantes(request):
    print request.user.get_all_permissions()
    estudiantes = None
    if request.user.has_perm('registros.admin_prac') or request.user.has_perm('registros.admin_vinc'):
        estudiantes = Estudiante.objects.all()
    elif request.user.has_perm('registros.resp_prac') or request.user.has_perm('registros.resp_vinc'):
        estudiantes = Estudiante.objects.filter(carrera=request.user.perfil.carrera)
    context = {
        'estudiantes' : estudiantes,
        'title': 'ESTUDIANTES'
    }
    return render(request, 'tablas/estudiantes.html', context)

@login_required
@permission_required('registros.view_coordinador')
def tabla_coordinadores(request):
    coordinadores = Coordinador.objects.all()
    context = {
        'coordinadores': coordinadores
    }
    return render(request, 'tablas/coordinadores.html', context)

@login_required
@permission_required('registros.web_services')
@transaction.atomic
def web_services(request):
    try:
        carreras()
        estudiantes()
        docentes()
        secciones()
        messages.success(request, 'Sus datos se han actualizado exitosamente.')
    except :
        messages.error(request, 'Error al obtener los datos. Por favor vuelva a intentarlo.')
    return redirect('registro:tabla_registros')

def carreras():
    carreras = _.get_data(_._carreras)
    for carrera in carreras:
        if not Carrera.objects.filter(codigo=carrera['codigo']).exists():
            instance = Carrera()
            instance.codigo = carrera['codigo']
            instance.nombre = carrera['nombre']
            instance.save()

def estudiantes():
    carreras = Carrera.objects.all()
    for carrera in carreras:
        estudiantes = _.get_data(_._listadoEstudiantesCarrera, carrera.codigo)
        if estudiantes:
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
    print 'ok'
    docentes = _.get_data(_._listadoDocentesPeriodoActual)
    for docente in docentes:
        if not Docente.objects.filter(cedula=docente['cedula']).exists():
            instance = Docente()
            instance.nombres = docente['nombres']
            instance.apellidos = docente['apellidos']
            instance.cedula = docente['cedula']
            instance.telefono = docente['telefono']
            instance.save()

def secciones():
    secciones = _.get_data(_._secciones)
    for seccion in secciones:
        if not Seccion.objects.filter(identificador=seccion['identificador']).exists():
            instance = Seccion()
            instance.identificador = seccion['identificador']
            instance.nombre = seccion['nombre']
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
        estudiante = get_object_or_404(Estudiante, pk=request.POST.get('pk'))
        data = {
            'nombres': estudiante.nombres,
            'apellidos': estudiante.apellidos,
            'cedula': estudiante.cedula,
        }
        return JsonResponse(data)
    raise Http404

@login_required
def ajax_entidad(request):
    if request.is_ajax():
        entidades = Entidad.objects.filter(carreras=request.POST.get('pk'))
        context = {
            'entidades' : [{'id':entidad.id, 'nombre':entidad.__unicode__()} for entidad in entidades]
        }
        return JsonResponse(context)
    raise Http404

@login_required
def ajax_empresa_estudiante(request):
    if request.is_ajax():
        empresas = Empresa.objects.filter(carreras=request.POST.get('pk'))
        estudiantes = Estudiante.objects.filter(carrera=request.POST.get('pk'))
        context = {
            'empresas' : [{'id':empresa.id, 'nombre':empresa.__unicode__()} for empresa in empresas],
            'estudiantes': [{'id':estudiante.id, 'nombre':estudiante.__unicode__()} for estudiante in estudiantes]
        }
        return JsonResponse(context)
    raise Http404

@login_required
def ajax_entidad_estudiante(request):
    if request.is_ajax():
        entidades = Entidad.objects.filter(carreras=request.POST.get('pk'))
        estudiantes = Estudiante.objects.filter(carrera=request.POST.get('pk'))
        context = {
            'entidades' : [{'id':entidad.id, 'nombre':entidad.__unicode__()} for entidad in entidades],
            'estudiantes': [{'id':estudiante.id, 'nombre':estudiante.__unicode__()} for estudiante in estudiantes]
        }
        return JsonResponse(context)
    raise Http404

@login_required
def ajax_evidencia_estudiante(request):
    if request.is_ajax():
        estudiante = get_object_or_404(Estudiante, id=request.POST.get('id'))
        data = []
        for practicas in estudiante.registros_practicas.all():
            data.append({
                'nombre' : practicas.empresa.nombre,
                'imagen' : [evidencia.imagen.url for evidencia in practicas.evidencias_registro_practicas.all()],
            })
        return JsonResponse(data, safe=False)
    raise Http404

def error(request):
    form = ErrorForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            form.save(request.user)
            messages.success(request, u'Mensaje enviado.')
            return redirect('index')
        except :
            messages.error(request, u'Conexión fallida!')
    elif request.POST:
        messages.error(request, u'Error al llenar el formulario.')
    context = {
        'form': form
    }
    return render(request, 'formulario.html', context)
    

def create_backup(request):
    try:
        from django.core.management import call_command
        call_command('dbbackup')
        try:
            call_command('mediabackup')
        except:
            print 'No existe media'
        messages.success(request, u'Respaldo creado exitosamente!')
    except:
        messages.error(request, u'Existio algun error!')
    return redirect('/')

def download_backup(request):
    from django.http import HttpResponse
    from django.conf import settings
    import StringIO
    import zipfile
    from os import listdir
    try:
        s = StringIO.StringIO()
        zf = zipfile.ZipFile(s, "w")
        list_backups = listdir(settings.PATH_BACKUP)
        for archivo in list_backups:
            name = archivo
            url = settings.PATH_BACKUP+'/'+archivo
            zf.write(url.encode('utf-8').strip(), name)
        zf.close()
        response = HttpResponse(s.getvalue(), content_type="application/zip")
        response['Content-Disposition'] = u'attachment; filename=evidencia_{}.zip'.format(list_backups[-1])
        return response
    except :
        messages.error(request, u'No se encuentra registros actualmente')
        return redirect('/')


### Funciones que solo sirven en desarrollo
@login_required
def flush_permisos(request):
    from django.contrib.auth.models import User
    from ..modulos import permisos
    for user in User.objects.all():
        if user.has_perm('registros.admin_prac'):
            user.user_permissions = permisos.administrador_practicas()
        elif user.has_perm('registros.resp_prac'):
            user.user_permissions = permisos.responsable_practicas()
        elif user.has_perm('registros.admin_vinc'):
            user.user_permissions = permisos.administrador_vinculacion()
        elif user.has_perm('registros.resp_vinc'):
            user.user_permissions = permisos.responsable_vinculacion()
    return redirect('/')

def update(): # Funcion utilzada ṕara las tareas de actualizacion
    cron_jobs.oficina()