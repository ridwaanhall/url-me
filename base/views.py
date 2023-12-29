# base/views.py
# from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import ShortenedURL
from .forms import ShortenedURLForm

def form_page(request):
    success_message = None

    if request.method == 'POST':
        long_url = request.POST.get('long_url')
        custom_domain = request.POST.get('custom_domain')
        custom_path = request.POST.get('custom_path')

        message = ShortenedURL(long_url=long_url, custom_domain=custom_domain, custom_path=custom_path)
        message.save()

        success_message = f'Message sent successfully! with custom_path {custom_path} and custom_domain {custom_domain}'

        return redirect('form_page')

    sidebar_data = ShortenedURL.objects.first()

    context = {
        'sidebar_data': sidebar_data,
        'success_message': success_message,
    }

    return render(request, 'base/form.html', context)


def form_pagea(request):
    if request.method == 'POST':
        form = ShortenedURLForm(request.POST)
        if form.is_valid():
            # Handle form submission (save to the database, etc.)
            # Example: shortened_url = form.save()

            # Redirect or render a success page
            return redirect('form_page')
    else:
        form = ShortenedURLForm()

    return render(request, 'base/form.html', {'form': form})


def redirect_custom_path(request, custom_path):
    shortened_url = get_object_or_404(ShortenedURL, custom_path=custom_path)
    return redirect(shortened_url.long_url)
