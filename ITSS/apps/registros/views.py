# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .form_create import RootForm


@login_required
@permission_required('user.add_user', login_url="/")
def crear_usuario(request):
    form = RootForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()  # cargar la instancia de perfil creada por la señal
        user.perfil.avatar = form.cleaned_data.get('avatar')
        user.perfil.cedula = form.cleaned_data.get('cedula')
        user.save()
        return redirect('index')
    context = {
        'form': form,
        'title': 'CREAR USUARIO'
    }
    return render(request, 'formularios/crear_usuario.html', context)