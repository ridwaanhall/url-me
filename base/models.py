from django.db import models
import random
import string

def generate_random_path():
    letters = string.ascii_letters
    random_leters = random.choice(letters)
    letters_and_digits = string.ascii_letters + string.digits
    return random_leters + ''.join(random.choice(letters_and_digits) for i in range(5))


class ShortenedURL(models.Model):
    long_url = models.URLField()
    custom_domain = models.URLField(blank=True, 
                                    null=True)
    custom_path = models.CharField(max_length=20, 
                                   unique=True, 
                                   blank=True, 
                                   null=True, 
                                   default=generate_random_path)

    def save(self, *args, **kwargs):
        if not self.custom_domain:
            self.custom_domain = "https://url.erbyl.repl.co"

        if self.custom_path and self.custom_path[0].isdigit():
            self.custom_path = self.custom_path

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Short URL: {self.custom_domain}/{self.custom_path}" if self.custom_domain else f"Short URL: {self.custom_path}"
