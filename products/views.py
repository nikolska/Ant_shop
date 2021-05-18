from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, render
from django.views.generic import DetailView, ListView, View

from .mixins import CartMixin
from .models import Ant, CartProduct, Category, LatestProducts, Formicary, Subcategory


CT_MODEL_MODEL_CLASS = {
    'ants': Ant,
    'formicaries': Formicary
}

class AddToCartView(CartMixin, View):
    CT_MODEL_MODEL_CLASS = {
        'ants': 'ant',
        'formicaries': 'formicary'
    }

    def get(self, request, *args, **kwargs):
        ct_model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        product_slug = kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            customer=self.cart.owner,
            cart=self.cart,
            content_type=content_type,
            object_id=product.id
        )
        if created:
            self.cart.products.add(cart_product)
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = {'cart': self.cart}
        return render(request, 'cart_view.html', ctx)


class HomePageView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = {
            'cart': self.cart,
            'categories': get_list_or_404(Category),
            'products': LatestProducts.objects.get_products_for_main_page('ant', 'formicary'),
            'subcategories': get_list_or_404(Subcategory),  
        }
        return render(request, 'base.html', ctx)



class ProductDetailView(CartMixin, DetailView):
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        self.model = CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['ct_model'] = self.model._meta.model_name
        return ctx


class ProductListView(CartMixin, ListView):
    template_name = 'product_list.html'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        model = CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.model = Subcategory.objects.get(slug=kwargs['category'])
        self.queryset = model.objects.filter(category=self.model)
        return super().dispatch(request, *args, **kwargs)

