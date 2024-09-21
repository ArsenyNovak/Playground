from django.shortcuts import render
from django.views.generic import ListView

from . models import Category


# Create your views here.

class HomePage(ListView):
    model = Category
    template_name = 'SportsGrounds/index.html'
    title_page = 'Главная страница'
    context_object_name = 'categories'