"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from jedzonko import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.IndexView.as_view(), name='index'),
    path('main/', v.MainView.as_view(), name='main'),
    path('recipe/<int:id>/', v.RecipeView.as_view(), name='recipe'),
    path('recipe/list/', v.RecipeListView.as_view(), name='recipe-list'),
    path('recipe/add/', v.AddRecipeView.as_view(), name='add-recipe'),
    path('recipe/modify/<int:id>/', v.ModifyRecipeView.as_view(), name='modify-recipe'),
    path('plan/list/', v.PlanListView.as_view(), name='plan-list'),
    path('plan/<int:id>/', v.PlanView.as_view(), name='plan'),
    path('plan/add/', v.AddPlanView.as_view(), name='add-plan'),
    path('plan/add-recipe/', v.PlanAddRecipeView.as_view(), name='plan-add-recipe')

]
