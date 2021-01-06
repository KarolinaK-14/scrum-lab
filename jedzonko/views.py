from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
import random

from .models import Recipe


class LandingPage(View):
    def get(self, request):

        name = request.GET.get('name')
        description = request.GET.get('description')


        recipe = Recipe.objects.all()
        recipe_list = list(recipe)
        random.shuffle(recipe_list)
        recipe_1 = recipe_list[0]
        recipe_2 = recipe_list[1]
        recipe_3 = recipe_list[2]
        name_1 = recipe_1.name
        name_2 = recipe_2.name
        name_3 = recipe_3.name
        description_1 = recipe_1.description
        description_2 = recipe_2.description
        description_3 = recipe_3.description

        ctx = {
            "name_1": name_1,
            "name_2": name_2,
            "name_3": name_3,
            "description_1": description_1,
            "description_2": description_2,
            "description_3": description_3
            }

        return render(request, "index.html", ctx)






class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


class RecipeListView(View):

    def get(self, request):
        return render(request, "app-recipes.html")


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
        description_add = request.POST.get('description_add')


        if name !="" and ingredients !="" and description !="" and preparation_time !="" and description_add !="":
            description += f"\n{description_add}"

            recipe = Recipe(name=name, ingredients=ingredients, description=description, preparation_time=preparation_time)
            recipe.save()

            # example = f"{recipe.name}, {recipe.ingredients}, {recipe.description}, {recipe.preparation_time}"
            # return HttpResponse(example)

            return redirect('recipe-list')
        
        error = {
            "error_msg": "wszystkie pola powinny być wypełnione!"
        }

        return render(request, 'app-add-recipe.html', error)

