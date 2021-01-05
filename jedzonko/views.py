from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .models import Recipe


class LandingPageView(View):
    def get(self, request):
        return render(request, "index.html")


class DashboardView(View):
    def get(self, request):
        return render(request, "dashboard.html")


class RecipeListView(View):
    def get(self, request):
        return render(request, "app-recipes.html")


class AddRecipeView(View):
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


class RecipeView(View):
    def get(self, request, recipe_id):
        return HttpResponse()


class ModifyRecipeView(View):
    def get(self, request, recipe_id):
        return HttpResponse()


class PlanListView(View):
    def get(self, request):
        return HttpResponse()


class PlanView(View):
    def get(self, request, plan_id):
        return HttpResponse()


class AddPlanView(View):
    def get(self, request):
        return HttpResponse()


class PlanAddRecipeView(View):
    def get(self, request):
        return HttpResponse()
