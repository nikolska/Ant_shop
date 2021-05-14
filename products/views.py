from django.shortcuts import get_list_or_404, render
# from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .models import Ant, Category, Formicary, Product, Subcategory


class HomePageView(TemplateView):
    template_name = 'home_page.html'


class ProductDetailView(DetailView):
    CT_MODEL_MODEL_CLASS = {
        'ants': Ant,
        'formicaries': Formicary
    }
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)


class ProductListView(ListView):
    CT_MODEL_MODEL_CLASS = {
        'ants': Ant,
        'formicaries': Formicary
    }
    template_name = 'product_list.html'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.model = Subcategory.objects.get(slug=kwargs['category'])
        self.queryset = model.objects.filter(category=self.model)
        return super().dispatch(request, *args, **kwargs)

