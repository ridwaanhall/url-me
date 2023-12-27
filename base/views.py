# base/views.py
from django.http import HttpResponse
from django.shortcuts import render

def hello_world(request):
    return render(request, 'base/form.html')
