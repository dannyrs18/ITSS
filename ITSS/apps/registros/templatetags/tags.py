# coding: utf-8
from django import template
from django.contrib.auth.models import User, Permission

register = template.Library()

@register.assignment_tag
def count_valores_practicas(lista):
    horas = 0
    calificacion = 0
    for value in lista:
        calificacion += value.calificacion
        horas += value.horas
    if calificacion:
        calificacion /= lista.count()
    return {'horas':horas, 'calificacion': "{0:.1f}".format(calificacion)}

@register.assignment_tag
def count_valores_vinculacion(lista):
    horas = 0
    calificacion = 0
    count = 0
    aux = []
    for value in lista:
        horas += value.total_horas
        calificacion += value.promedio
        aux.append(value.componente.proyecto_vinculacion)
    if lista:
        calificacion /= lista.count()
        count = len(set(aux))
    return {'horas':horas, 'calificacion': "{0:.1f}".format(calificacion), 'count':count}

@register.assignment_tag
def mess(messages):
    data = []
    if messages:
        for message in messages:
            data.append({
                'title': message.tags,
                'message': message
            })
        data = data[0]
    return data

@register.assignment_tag
def component(proyecto):
    # EL ESTADO 2 ES POR DEFAULT NO COMPLETADO
    # EL ESTADO 1 ES PENDIENTE
    # EL ESTADO 0 ES REALIZADO
    if proyecto:
        if not proyecto.componentes.filter(estado=1).exists() and proyecto.componentes.filter(estado=2).exists():
            componente = proyecto.componentes.filter(estado=2).first()
            componente.estado = 1
            componente.save()
    
@register.filter
def permisos(usuario):
    permiso = ''
    if Permission.objects.get(codename='admin_prac').user_set.filter(id=usuario.id).exists():
        permiso = 'Administrador de practicas'
    elif Permission.objects.get(codename='admin_vinc').user_set.filter(id=usuario.id).exists():
        permiso = 'Administrador de vinculación'
    if Permission.objects.get(codename='resp_prac').user_set.filter(id=usuario.id).exists() | Permission.objects.get(codename='resp_vinc').user_set.filter(id=usuario.id).exists():
        permiso = 'Responsable de {}'.format(usuario.perfil.carrera)
    return permiso