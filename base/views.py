# base/views.py
# from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import ShortenedURL
from .forms import ShortenedURLForm


def form_page(request):

    if request.method == 'POST':
        custom_path = request.POST.get('custom_path')
    
        # Check if the custom path is in the disallowed list
        disallowed_paths = [
            "admin", "login", "logout", "wp-admin", "wp-login", "dashboard", "controlpanel", "adminpanel", "cpanel",
            "root", "superuser", "moderator", "settings", "config", "secure", "account", "register", "signup", "join",
            "submit", "create", "edit", "delete", "remove", "manage", "download", "upload", "uploadfile", "file",
            "image", "picture", "media", "script", "script.js", "style", "style.css", "api", "webhook", "callback",
            "oauth", "token", "key", "secret", "auth", "password", "reset", "verify", "email", "newsletter", "contact",
            "feedback", "support", "help", "faq", "terms", "privacy", "cookie", "about", "blog", "news", "press",
            "events", "partners", "jobs", "careers", "advertise", "sponsor", "affiliate", "shop", "store", "checkout",
            "cart", "buy", "purchase", "order", "payment", "invoice", "billing", "shipping", "delivery", "subscribe",
            "unsubscribe", "notification", "alert", "warning", "error", "debug", "test", "trial", "demo", "example",
            "sample", "sandbox", "staging", "production", "live", "localhost", "127.0.0.1",
        ]
    
        if custom_path in disallowed_paths:
            messages.error(request, 'Custom path not allowed.')
            return redirect('form_page')
    
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
