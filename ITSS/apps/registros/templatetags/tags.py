from django import template

register = template.Library()

@register.assignment_tag
def count_valores(lista):
    horas = 0
    calificacion = 0
    for value in lista:
        calificacion += value.calificacion
        horas += value.horas
    if calificacion:
        calificacion /= lista.count()
    return {'horas':horas, 'calificacion': "{0:.1f}".format(calificacion)}