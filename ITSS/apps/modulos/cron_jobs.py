
from ..practicas.models import Empresa
from ..vinculacion.models import Entidad
def oficina():
    print localtime(now()).date()
    for entidad in Entidad.objects.all():
        if localtime(now()).date() >= entidad.fin and estado == True:
            entidad.estado = False
            entidad.save()
    for empresa in Empresa.objects.all():
        if localtime(now()).date() >= empresa.fin and estado == True:
            empresa.estado = False
            empresa.save()
            