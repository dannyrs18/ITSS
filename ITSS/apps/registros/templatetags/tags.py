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
    if proyecto:
        print proyecto
        componentes = proyecto.componentes.all()
        realizados = componentes.filter(estado=0)
        proceso = componentes.filter(estado=1)
        if not realizados and not proceso:
            componente = componentes.filter(estado=2).first()
            componente.estado = 1
            componente.save()
    
        
