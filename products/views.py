from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import CategoryForm
from .models import Category, Product


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')


class CategoryListView(ListView):
    model = Category


class CategoryView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        products = Product.objects.filter(category_id=self.kwargs['pk'])
        ctx = super().get_context_data(**kwargs)
        ctx["products"] = products
        return ctx


class ProductView(DetailView):
    model = Product
