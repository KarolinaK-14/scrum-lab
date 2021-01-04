from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request):
        return render(request, "index.html")


class RecipeListView(View):

    def get(self, request):
        return render(request, "app-recipes.html")
