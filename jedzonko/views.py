from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
import random
from .models import Recipe, Plan, RecipePlan
from .enums import DayName


class LandingPageView(View):
    def get(self, request):
        recipe = Recipe.objects.all()
        recipe_list = list(recipe)
        random.shuffle(recipe_list)

        EMPTY_INFO = ("Tu może być twój przepis", "aby dodać przepis, przejdź do listy przepisów")

        recipes_carousel = recipe_list[:3]
        while len(recipes_carousel) < 3:
            recipes_carousel.append(EMPTY_INFO)

        ctx = {
            "recipes": recipes_carousel,
            "empty_info_name": EMPTY_INFO[0],
            "empty_info_description": EMPTY_INFO[1]
        }

        return render(request, "index.html", ctx)


class DashboardView(View):
    def get(self, request):
        recipes = Recipe.objects.all().count()
        plans = Plan.objects.all()
        plans_count = plans.count()

        try:
            last_plan = plans.order_by("-created")[0]
        except IndexError:
            return render(request, "dashboard.html", {"recipes_number": recipes, "plans_number": plans_count})

        last_plan_recipes = last_plan.recipeplan_set.all().order_by("order")
        unique_days = list({i.day_name for i in last_plan_recipes})
        day_name_list = DayName.values()
        sorted_days_index = sorted([day_name_list.index(unique_days[i]) for i in range(len(unique_days))])
        sorted_days_name = [day_name_list[i] for i in sorted_days_index]
        context = {
            "recipes_number": recipes,
            "plans_number": plans_count,
            "plan": last_plan,
            "plan_recipes": last_plan_recipes,
            "days": sorted_days_name
        }
        return render(request, "dashboard.html", context=context)


class RecipeListView(View):
    def get(self, request):
        recipe_list = Recipe.objects.all().order_by("-votes", "-created")
        paginator = Paginator(recipe_list, 50)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, "app-recipes.html", {"recipes": recipes})


class ModifyRecipeView(View):
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        return render(request, "app-edit-recipe.html", {"recipe": recipe})

    def post(self, request, recipe_id):
        name = request.POST.get("name")
        ingredients = request.POST.get("ingredients")
        description = request.POST.get("description")
        preparation = request.POST.get("preparation")
        preparation_time = request.POST.get("preparation_time")

        if name and ingredients and description and preparation and preparation_time:
            Recipe.objects.create(name=name,
                                ingredients=ingredients,
                                description=description,
                                preparation=preparation,
                                preparation_time=preparation_time)
            return redirect('recipe-list')

        error = {
            "error_msg": "Wypełnij poprawnie wszystkie pola",
            "recipe": Recipe.objects.get(pk=recipe_id)
        }
        return render(request, 'app-edit-recipe.html', error)


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

        if name != "" and ingredients != "" and description != "" and preparation_time != "" and description_add != "":
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
        plan_list = Plan.objects.all().order_by("-name", "-created")
        paginator = Paginator(plan_list, 1)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        return render(request, "app-schedules.html", {"plans": plans})


class PlanView(View):
    def get(self, request, plan_id):
        return render(request, "app-details-schedules.html")


class AddPlanView(View):
    """
        use it to add new Plan
    """
    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name != "" and description != "":
            plan = Plan(name=name,
                        description=description,
                        )
            plan.save()
            return redirect('plan-list')

        error = {
            "error_msg": "wszystkie pola powinny być wypełnione!"
        }

        return render(request, 'app-add-schedules.html', error)


class RecipeView(View):
    def get(self, request, recipe_id):
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
            'id': recipe.id,
        }
        return render(request, "app-recipe-details.html", context)

    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        if 'just_liked' in request.POST:
            recipe.votes += 1
        elif 'not_liked' in request.POST:
            recipe.votes -= 1

        recipe.save()
        return redirect('recipe', recipe_id)


class PlanAddRecipeView(View):
    def get(self, request):
        context = {
            "plans" : list(Plan.objects.all()),
            "recipes" : list(Recipe.objects.all()),
        }

        return render(request, "app-schedules-meal-recipe.html", context)
    
    def post(self, request):
        plan_id = request.POST.get('choosePlan')
        meal_name = request.POST.get('name')
        meal_number = request.POST.get('number')
        recipe_id = request.POST.get('recipe_id')
        day = request.POST.get('day')

        if plan_id and meal_name and meal_number and recipe_id and day:

            plan_id = int(plan_id)
            recipe_id = int(recipe_id)
            meal_number = int(meal_number)

            recipe = Recipe.objects.get(id=recipe_id)
            plan = Plan.objects.get(id=plan_id)

            # plan.recipes.add(recipe, trough_defaults = {'meal_name':meal_name, 'plan':plan, 'order':meal_number, 'day_name':day})

            recipe_plan = RecipePlan(
                meal_name=meal_name,
                recipe=recipe,
                plan=plan,
                order=meal_number,
                day_name=day
            )

            recipe_plan.save()

            return redirect('plan', plan_id)


        context = {
            "plans" : list(Plan.objects.all()),
            "recipes" : list(Recipe.objects.all()),
            "error_msg" : "Wszystkie pola muszą być wypełnione"
        }

        # context["error_msg"] = f"plan_id: {plan_id}, meal_name: {meal_name}, meal_number: {meal_number}, recipe_id: {recipe_id}, day: {day}"

        return render(request, "app-schedules-meal-recipe.html", context)
