from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import CategoryForm
from .models import Category, Product


class CategoryCreateView(CreateView):
    model = Category
    success_url = reverse_lazy('category')


class CategoryListView(ListView):
    model = Category


class CategoryView(DetailView):
    model = Category


