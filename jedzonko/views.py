from datetime import datetime

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .models import Recipe


class LandingPage(View):
    def get(self, request):
        return render(request, "index.html")


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class AddRecipe(View):
    """
    use it to add new Recipe
    """
    
    def get(self, request):
        return render(request, 'app-add-recipe.html')
    
    def post(self, request):
        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')

        if name !="" and ingredients !="" and description !="" and preparation_time !="":
            recipe = Recipe(name=name, ingredients=ingredients, description=description, preparation_time=preparation_time)
            recipe.save()
            
            # example = f"{new_recipe.name}, {new_recipe.ingredients}, {new_recipe.description}, {new_recipe.preparation_time}"
            # return HttpResponse(example)

            return render(request, 'app-recipes.html')
        
        error = {
            "error_msg": "wszystkie pola powinny być wypełnione!"
        }

        return render(request, 'app-add-recipe.html', error)