from django.contrib.auth.models import Permission

def administrador_practicas():
    perms = (
        Permission.objects.get(codename='view_coordinador'),
        Permission.objects.get(codename='add_coordinador'),
        Permission.objects.get(codename='change_user'),
        Permission.objects.get(codename='add_informe_practicas'),
        Permission.objects.get(codename='view_estudiante'),
        Permission.objects.get(codename='view_perfil'),
        Permission.objects.get(codename='add_user'),
        Permission.objects.get(codename='view_empresa'),
        Permission.objects.get(codename='add_empresa'),
        Permission.objects.get(codename='change_empresa'),
        Permission.objects.get(codename='view_registro_practicas'),
        Permission.objects.get(codename='change_registro_practicas'),
        Permission.objects.get(codename='view_informe_practicas'),
        Permission.objects.get(codename='view_reportes'),
        Permission.objects.get(codename='reporte_estudiante'),
        Permission.objects.get(codename='reporte_empresa'),
        Permission.objects.get(codename='reporte_registro_practicas'),
        Permission.objects.get(codename='reporte_convenio_practicas'),
        Permission.objects.get(codename='add_registro_practicas'),
        Permission.objects.get(codename='admin_prac'),
    )
    return perms

def administrador_vinculacion():
    perms = (
        Permission.objects.get(codename='view_coordinador'),
        Permission.objects.get(codename='change_user'),
        Permission.objects.get(codename='view_estudiante'),
        Permission.objects.get(codename='view_perfil'),
        Permission.objects.get(codename='add_user'),
        Permission.objects.get(codename='view_proyecto_vinculacion'),
        Permission.objects.get(codename='add_proyecto_vinculacion'),
        Permission.objects.get(codename='add_componente'),
        Permission.objects.get(codename='view_actividad_vinculacion'),
        Permission.objects.get(codename='add_actividad_vinculacion'),
        Permission.objects.get(codename='view_entidad'),
        Permission.objects.get(codename='add_entidad'),
        Permission.objects.get(codename='view_informe_vinculacion'),
        Permission.objects.get(codename='add_informe_vinculacion'),
        Permission.objects.get(codename='reporte_convenio_vinculacion'),
        Permission.objects.get(codename='change_entidad'),
        Permission.objects.get(codename='view_reportes'),
        Permission.objects.get(codename='reporte_estudiante'),
        Permission.objects.get(codename='reporte_entidad'),
        Permission.objects.get(codename='reporte_registro_proyectos'),
        Permission.objects.get(codename='admin_vinc'),
    )
    return perms

def responsable_practicas():
    perms = (
        Permission.objects.get(codename='view_coordinador'),
        Permission.objects.get(codename='change_user'),
        Permission.objects.get(codename='view_estudiante'),
        Permission.objects.get(codename='view_empresa'),
        Permission.objects.get(codename='add_empresa'),
        Permission.objects.get(codename='view_registro_practicas'),
        Permission.objects.get(codename='add_registro_practicas'),
        Permission.objects.get(codename='change_registro_practicas'),
        Permission.objects.get(codename='change_empresa'),
        Permission.objects.get(codename='reporte_convenio_practicas'),
        Permission.objects.get(codename='view_reportes'),
        Permission.objects.get(codename='reporte_estudiante'),
        Permission.objects.get(codename='reporte_empresa'),
        Permission.objects.get(codename='resp_prac'),
    )
    return perms

def responsable_vinculacion():
    perms = (
        Permission.objects.get(codename='view_coordinador'),
        Permission.objects.get(codename='change_user'),
        Permission.objects.get(codename='view_actividad_vinculacion'),
        Permission.objects.get(codename='add_actividad_vinculacion'),
        Permission.objects.get(codename='view_proyecto_vinculacion'),
        Permission.objects.get(codename='add_proyecto_vinculacion'),
        Permission.objects.get(codename='add_componente'),
        Permission.objects.get(codename='view_estudiante'),
        Permission.objects.get(codename='view_entidad'),
        Permission.objects.get(codename='add_entidad'),
        Permission.objects.get(codename='view_reportes'),
        Permission.objects.get(codename='resp_vinc'),
        Permission.objects.get(codename='reporte_convenio_vinculacion'),
        Permission.objects.get(codename='reporte_estudiante'),
        Permission.objects.get(codename='reporte_registro_proyectos'),
        Permission.objects.get(codename='change_entidad'),
    )
    return perms