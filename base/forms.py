from django import forms
from .models import ShortenedURL

class ShortenedURLForm(forms.ModelForm):
    class Meta:
        model = ShortenedURL
        fields = ['long_url', 'custom_domain', 'custom_path']