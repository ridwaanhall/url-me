# base/views.py
# from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import ShortenedURL
from .forms import ShortenedURLForm


def form_page(request):

    if request.method == 'POST':
        custom_path = request.POST.get('custom_path')

        try:
            existing_url = ShortenedURL.objects.get(custom_path=custom_path)
            messages.error(request, 'Custom path already exists.')
            return redirect('form_page')
        except ShortenedURL.DoesNotExist:
            pass

        form = ShortenedURLForm(request.POST)
        if form.is_valid():
            shortened_url = form.save(commit=False)
            shortened_url.clean()
            shortened_url.save()

            full_shortened_url = f'{shortened_url.custom_domain}/{shortened_url.custom_path}'
            messages.success(
                request,
                f'Shortened URL created successfully! {full_shortened_url}')
            return redirect('form_page')

    else:
        form = ShortenedURLForm()

    context = {
        'form': form,
    }
    
    return render(request, 'base/form.html', context)


def redirect_custom_path(request, custom_path):
    shortened_url = get_object_or_404(ShortenedURL, custom_path=custom_path)
    return redirect(shortened_url.long_url)
