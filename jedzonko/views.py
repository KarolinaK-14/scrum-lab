from datetime import datetime

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .models import Recipe


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


# class Login(View):

#     def get(self, request):
#         return render(request, 'exercises/login.html')

#     def post(self, request):
#         name = request.POST.get('name')
#         password = request.POST.get('password')
#         try:
#             User.objects.get(username = name, password = password)
#             response = HttpResponse('Zalogowano')
#             response.set_cookie("logged_in", "logged_in", max_age=24*60*60)
#             return response
#         except Exception:
#             response = HttpResponse(f"Błąd logowania")
#             response.delete_cookie("logged_in")
#             return response


class AddRecipe(View):
    """
    use it to add new Recipe
    """
    
    def get(self, request):
        return render(request, 'app-add-recipe.html')
    
    def post(self, request):
        new_recipe = Recipe()
        new_recipe.name = request.POST.get('name')
        new_recipe.ingredients = request.POST.get('ingredients')
        new_recipe.description = request.POST.get('description')
        new_recipe.preparation_time = request.POST.get('preparation_time')
        new_recipe.save()

        # example = f"{new_recipe.name}, {new_recipe.ingredients}, {new_recipe.description}, {new_recipe.preparation_time}"
        # return HttpResponse(example)

        return render(request, 'app-recipes.html')