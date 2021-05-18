from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, View

from .models import Ant, Cart, CartProduct, Customer, Formicary, Subcategory


class AddToCartView(View):
    CT_MODEL_MODEL_CLASS = {
        'ants': 'ant',
        'formicaries': 'formicary'
    }

    def get(self, request, *args, **kwargs):
        ct_model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        product_slug = kwargs.get('slug')
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer, in_order=False)
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            customer=cart.owner,
            cart=cart,
            content_type=content_type,
            object_id=product.id, 
            final_price=product.price
        )
        cart.products.add(cart_product)
        return HttpResponseRedirect('/cart/')


class CartView(View):
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        ctx = {'cart': cart}
        return render(request, 'cart_view.html', ctx)


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
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['ct_model'] = self.model._meta.model_name
        return ctx


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

