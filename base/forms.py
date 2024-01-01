from django import forms
from .models import ShortenedURL

class ShortenedURLForm(forms.ModelForm):
    class Meta:
        model = ShortenedURL
        fields = ['long_url', 'custom_domain', 'custom_path']

    def clean_custom_path(self):
        custom_path = self.cleaned_data.get('custom_path')

        # Check if the custom path already exists in the database
        if ShortenedURL.objects.filter(custom_path=custom_path).exists():
            raise forms.ValidationError('Custom path already exists.')

        return custom_path