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


# class CategoryCreateView(CreateView):
#     model = Category
#     form_class = CategoryForm
#     success_url = reverse_lazy('category_list')


# class CategoryListView(ListView):
#     model = Category

#     def get_context_data(self, **kwargs):
#         subcategories = Subcategory.objects.all()
#         ctx = super().get_context_data(**kwargs)
#         ctx["subcategories"] = subcategories
#         return ctx


# class ProductCreateView(CreateView):
#     model = Product
#     form_class = ProductForm
#     success_url = reverse_lazy('product_list')


# class ProductListView(ListView):
#     model = Subcategory
#     template_name = 'products/product_list.html'

#     def get_context_data(self, **kwargs):
#         products = Product.objects.filter(subcategory_id=self.kwargs['pk'])
#         ctx = super().get_context_data(**kwargs)
#         ctx["products"] = products
#         return ctx


# class SubcategoryCreateView(CreateView):
#     model = Subcategory
#     form_class = SubcategoryForm
#     success_url = reverse_lazy('subcategory_list')

