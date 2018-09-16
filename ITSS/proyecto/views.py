# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

def login(request):
    username = request.POST.getlist('username')
    password = request.POST.getlist('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        redirect('index')
    render(request, 'login.html')