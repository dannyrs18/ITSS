from django.contrib.auth.models import Permission

def administrador_practicas():
    perms = (
        Permission.objects.get(codename='view_informe_practicas'),
        Permission.objects.get(codename='add_informe_practicas'),
        Permission.objects.get(codename='view_estudiante'),
        Permission.objects.get(codename='view_perfil'),
        Permission.objects.get(codename='add_user'),
        Permission.objects.get(codename='view_empresa'),
        Permission.objects.get(codename='add_empresa'),
        Permission.objects.get(codename='view_registro_practicas'),
        Permission.objects.get(codename='change_registro_practicas'),
        Permission.objects.get(codename='admin_prac'),
    )
    return perms

def administrador_vinculacion():
    perms = None
    return perms

def responsable_practicas():
    perms = (
        Permission.objects.get(codename='view_estudiante'),
        Permission.objects.get(codename='view_empresa'),
        Permission.objects.get(codename='add_empresa'),
        Permission.objects.get(codename='view_registro_practicas'),
        Permission.objects.get(codename='add_registro_practicas'),
        Permission.objects.get(codename='change_registro_practicas'),
        Permission.objects.get(codename='resp_prac'),
    )
    return perms

def responsable_vinculacion():
    perms = None
    return perms