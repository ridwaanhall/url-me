from django.core.exceptions import ValidationError
from django.db import models
import random
import string

def generate_random_path():
    letters = string.ascii_letters
    random_letters = random.choice(letters)
    letters_and_digits = string.ascii_letters + string.digits
    return random_letters + ''.join(random.choice(letters_and_digits) for _ in range(4))

class ShortenedURL(models.Model):
    long_url = models.URLField()
    custom_domain = models.URLField(blank=True, null=True)
    custom_path = models.CharField(max_length=20, unique=True, blank=True, null=True, default=generate_random_path)

    def clean(self):
        forbidden_domains = [
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

        if self.custom_domain and any(domain in self.custom_domain.lower() for domain in forbidden_domains):
            raise ValidationError("Custom domain is not allowed. Choose a different one.")

    def save(self, *args, **kwargs):
        self.clean()

        if not self.custom_domain:
            self.custom_domain = "https://url.erbyl.repl.co"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Short URL: {self.custom_domain}/{self.custom_path}" if self.custom_domain else f"Short URL: {self.custom_path}"
