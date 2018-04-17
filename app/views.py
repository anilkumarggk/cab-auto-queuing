# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


# Create your views here.
def index_view(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def userapp_view(request):
    if request.method == 'GET':
        return render(request, 'userapp.html')


def driverapp_view(request):
    if request.method == 'GET':
        return render(request, 'driverapp.html')


def dashboard_view(request):
    if request.method == 'GET':
        return render(request, 'dashboard.html')
