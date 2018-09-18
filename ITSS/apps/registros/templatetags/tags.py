from django import template

register = template.Library()

@register.simple_tag
def oficina(user):
    if user.has_perm('practicas.add_empresa'):
        return 'Empresa'
    elif user.has_perm('vinculacion.add_entidad'):
        return 'Entidad'