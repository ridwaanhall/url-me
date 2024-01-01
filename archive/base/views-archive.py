# base/views.py
# from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import ShortenedURL
from django.urls import reverse
from .forms import ShortenedURLForm

# def form_page(request):
#     # long_url = models.URLField()
#     # custom_domain = models.URLField(blank=True, null=True)
#     # custom_path = models.CharField(max_length=20, unique=True, blank=True, null=True, default=generate_random_path)
#     if request.method == 'POST':
#         long_url = request.POST.get('long_url')
#         custom_domain = request.POST.get('custom_domain')
#         custom_path = request.POST.get('custom_path')

#         try:


#     return render(request, 'base/form.html', context)


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
            shortened_url.clean()  # Ensure model clean is executed
            shortened_url.save()   # Save to the database

            # Get the full URL of the created short URL
            full_shortened_url = f'{shortened_url.custom_domain}/{shortened_url.custom_path}'

            # Add a success flash message with the shortened URL
            messages.success(request, f'Shortened URL created successfully! {full_shortened_url}')

            # Redirect or render a success page
            return redirect('form_page')

    else:
        form = ShortenedURLForm()

    context = {
        'form': form,
        # 'full_shortened_url': full_shortened_url,
    }
    return render(request, 'base/form.html', context)


def redirect_custom_path(request, custom_path):
    shortened_url = get_object_or_404(ShortenedURL, custom_path=custom_path)
    return redirect(shortened_url.long_url)
