from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


class MainView(View):
    def get(self, request):
        return render(request, "dashboard.html")


class RecipeListView(View):
    def get(self, request):
        return HttpResponse()


class RecipeView(View):
    def get(self, request):
        return HttpResponse()


class AddRecipeView(View):
    def get(self, request):
        return HttpResponse()


class ModifyRecipeView(View):
    def get(self, request):
        return HttpResponse()


class PlanListView(View):
    def get(self, request):
        return HttpResponse()


class PlanView(View):
    def get(self, request):
        return HttpResponse()


class AddPlanView(View):
    def get(self, request):
        return HttpResponse()


class PlanAddRecipeView(View):
    def get(self, request):
        return HttpResponse()

