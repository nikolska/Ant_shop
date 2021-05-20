from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, View

from .models import Cart, Category, Customer, Product, Subcategory


class HomePageView(TemplateView):
    paginate_by = 3
    template_name = 'home_page.html'


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


class ProductListView(ListView):
    model = Product
    paginate_by = 3
    template_name = 'product_list.html'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        subcategory = Subcategory.objects.get(slug=kwargs['subcategory'])
        self.queryset = self.model.objects.filter(category=subcategory)
        return super().dispatch(request, *args, **kwargs)
