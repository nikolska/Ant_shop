from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import CategoryForm, SubcategoryForm
from .models import Category, Product, Subcategory


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')


class CategoryListView(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        subcategories = Subcategory.objects.all()
        ctx = super().get_context_data(**kwargs)
        ctx["subcategories"] = subcategories
        return ctx


class ProductListView(ListView):
    model = Subcategory
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        products = Product.objects.filter(subcategory_id=self.kwargs['pk'])
        ctx = super().get_context_data(**kwargs)
        ctx["products"] = products
        return ctx


class ProductView(DetailView):
    model = Product


class SubcategoryCreateView(CreateView):
    model = Subcategory
    form_class = SubcategoryForm
    success_url = reverse_lazy('subcategory_list')

