from django.db import models
from datetime import datetime

# Create your models here.

class Recipe(models.Model):
    """
      - name: nazwa przepisu,
  - ingredients: składniki przepisu,
  - description: treść przepisu,
  - preparation: sposób przygotowania przepisu,
  - created: data dodania przepisu (wypełniane automatycznie),
  - updated: data aktualizacji przepisu (wypełniane automatycznie),
  - preparation_time: czas przygotowania (w minutach),
  - votes: liczba głosów na przepis (domyślnie 0)
    """
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    preparation = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)
