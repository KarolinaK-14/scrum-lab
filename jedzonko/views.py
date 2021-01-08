from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
import random
from .models import Recipe


class LandingPageView(View):
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


class DashboardView(View):
    def get(self, request):
        recipes = Recipe.objects.all().count()
        context = {
            "recipes_number": recipes
        }
        return render(request, "dashboard.html", context=context)


class RecipeListView(View):
    def get(self, request):
        recipe_list = Recipe.objects.all().order_by("-votes", "-created")
        paginator = Paginator(recipe_list, 50)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, "app-recipes.html", {"recipes": recipes})


class RecipeView(View):
    def get(self, request, recipe_id):
        return HttpResponse()


class ModifyRecipeView(View):
    def get(self, request, recipe_id):
        return HttpResponse()


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

            recipe = Recipe(name=name,
                ingredients=ingredients,
                description=description,
                preparation_time=preparation_time,
                preparation=description_add,
            )
            recipe.save()

            # example = f"{recipe.name}, {recipe.ingredients}, {recipe.description}, {recipe.preparation_time}"
            # return HttpResponse(example)

            return redirect('recipe-list')
        
        error = {
            "error_msg": "wszystkie pola powinny być wypełnione!"
        }

        return render(request, 'app-add-recipe.html', error)


class PlanListView(View):
    def get(self, request):
        return HttpResponse()


class PlanView(View):
    def get(self, request):
        return render(request, "app-schedules.html")


class AddPlanView(View):
    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        return redirect('add-plan')


class RecipeView(View):
    def get (self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Exception:
            return redirect('add-recipe')
        context = {
            'name': recipe.name,
            'ingredients': recipe.ingredients,
            'description': recipe.description,
            'preparation': recipe.preparation,
            'preparation_time': recipe.preparation_time,
            'votes': recipe.votes,
            'id' : recipe.id,
        }
        return render(request, "app-recipe-details.html", context)
    
    def post (self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        if 'just_liked' in request.POST:
            recipe.votes += 1
        elif 'not_liked' in request.POST:
            recipe.votes -= 1
        
        recipe.save()
        return redirect('recipe', recipe_id)

class PlanAddRecipeView(View):
    def get(self, request):
        return HttpResponse()

