from django.db import models
from .enums import DayName
from django.template.defaultfilters import slugify


class Recipe(models.Model):
    """
    - name: nazwa przepisu,
    - ingredients: składniki przepisu,
    - description: treść przepisu,
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


class Plan(models.Model):
    """
    - name: nazwa planu,
    - description: opis planu,
    - created: data utworzenia.
    - recipes - relacja wiele do wielu do modelu przepisu (model pośredni recipeplan)
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through="RecipePlan")


class RecipePlan(models.Model):
    """
    - meal_name: nazwa posiłku (śniadanie, obiad itp),
    - recipe: relacja do tabeli przepisów
    - plan: relacja do tabeli planów
    - order: kolejność posiłków w planie,
    - day_name: "from .enums import DayName"
    """
    meal_name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()
    day_name = models.CharField(max_length=16, choices=DayName.choices())


class Page(models.Model):
    """
    - title: tytuł strony,
    - description: treść strony,
    - slug: unikalny identyfikator tworzony na podstawie tytułu
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)
