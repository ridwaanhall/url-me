# base/views.py
# from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import ShortenedURL


def hello_world(request):
    return render(request, 'base/form.html')

def redirect_custom_path(request, custom_path):
    shortened_url = get_object_or_404(ShortenedURL, custom_path=custom_path)
    return redirect(shortened_url.long_url)
