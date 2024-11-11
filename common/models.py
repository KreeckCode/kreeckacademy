from django.db import models
from django.utils.crypto import get_random_string

class APIKey(models.Model):
    key = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.key
    

# TO Generate the API Keys you have to run this command: python manage.py generate_api_keys --count 5 --activate
