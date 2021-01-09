from django.core.paginator import Paginator
from django.shortcuts import render, redirect
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

        ctx = {
            "name_1": EMPTY_INFO[0],
            "name_2": EMPTY_INFO[0],
            "name_3": EMPTY_INFO[0],
            "description_1": EMPTY_INFO[1],
            "description_2": EMPTY_INFO[1],
            "description_3": EMPTY_INFO[1],
        }

        if len(recipe_list) >= 1:
            recipe_1 = recipe_list[0]
            name_1 = recipe_1.name
            description_1 = recipe_1.description
            ctx["name_1"] = name_1
            ctx["description_1"] = description_1

            if len(recipe_list) >= 2:
                recipe_2 = recipe_list[1]
                name_2 = recipe_2.name
                description_2 = recipe_2.description
                ctx["name_2"] = name_2
                ctx["description_2"] = description_2

                if len(recipe_list) >= 3:
                    recipe_3 = recipe_list[2]
                    name_3 = recipe_3.name
                    description_3 = recipe_3.description
                    ctx["name_3"] = name_3
                    ctx["description_3"] = description_3

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
        return render(request, "app-schedules.html")


class PlanView(View):
    def get(self, request, plan_id):
        try:
            plan = Plan.objects.get(id=plan_id)
        except Exception:
            return redirect('add-plan')
        rec_plan = RecipePlan.objects.all()

        context = {
            'name': plan.name,
            'description': plan.description,

            #'dayname_1': rec_plan.DayName.MONDAY, # do odkomentowania jak pojawi sie dodawanie obiektów modelu RecipePlan
            #'dayname_2': rec_plan.DayName.TUESDAY,
            #'dayname_3': rec_plan.DayName.WEDNESDAY,
            #'dayname_4': rec_plan.DayName.THURSDAY,
            #'dayname_5': rec_plan.DayName.FRIDAY,
            #'dayname_6': rec_plan.DayName.SATURDAY,
            #'dayname_7': rec_plan.DayName.SUNDAY,
            #'meal_name': rec_plan.meal_name,
            #'recipe': rec_plan.recipe,
        }
        return render(request, "app-details-schedules.html", context)


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
        return render(request, "app-schedules-meal-recipe.html")
