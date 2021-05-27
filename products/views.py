from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import mail_admins, send_mail
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView, UpdateView, View

from .forms import ContactForm, CustomerCreateForm, CustomerUpdateForm
from .models import Cart, CartProduct, Customer, Product, Subcategory
from ant_shop.settings import EMAIL_HOST_USER


def get_customer_cart(request):
    if request.user.is_anonymous:
        cart = Cart.objects.filter(for_anonymous_user=True).first()
        if not cart:
            cart = Cart.objects.create(for_anonymous_user=True)
    else:
        customer = Customer.objects.get(username=request.user.username)
        cart = Cart.objects.filter(owner=customer, in_order=False).first()
    return cart


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.total_products = cart_data['id__count']
    cart.save()


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        cart = get_customer_cart(request)
        product = Product.objects.get(slug=kwargs.get('slug'))
        cart_product, created = CartProduct.objects.get_or_create(
            product=product,
            customer=request.user,
            cart=cart,
            final_price=product.price
        )
        if created:
            cart.products.add(cart_product)
        recalc_cart(cart)
        messages.add_message(request, messages.INFO, f'{product.title} added to cart')
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(View):
    def get(self, request, *args, **kwargs):
        cart = get_customer_cart(request)
        product = Product.objects.get(slug=kwargs.get('slug'))
        cart_product = CartProduct.objects.get(
            product=product,
            customer=request.user,
            cart=cart
        )
        cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(cart)
        messages.add_message(request, messages.INFO, f'{product.title} removed from cart')
        return HttpResponseRedirect('/cart/')


class ChangeProductQuantityView(View):
    def post(self, request, *args, **kwargs):
        cart = get_customer_cart(request)
        product = Product.objects.get(slug=kwargs.get('slug'))
        cart_product = CartProduct.objects.get(
            product=product,
            customer=request.user,
            cart=cart
        )
        product_quantity = int(request.POST.get('product_quantity'))
        cart_product.qty = product_quantity
        cart_product.save()
        recalc_cart(cart)
        messages.add_message(request, messages.INFO, f'Quantity of {product.title} changed')
        return HttpResponseRedirect('/cart/')


class CartView(View):
    def get(self, request, *args, **kwargs):
        cart = get_customer_cart(request)
        ctx = {'cart': cart}
        return render(request, 'cart_view.html', ctx)


class HomePageView(TemplateView):
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


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'contact_page.html'

    def form_valid(self, form):
        if self.request.user.id is not None:
            sender = self.request.user.full_name
            sender_email = self.request.user.email
        else:
            sender = form.cleaned_data['sender']
            sender_email = form.cleaned_data['sender_email']
        
        message = form.cleaned_data['message_text']

        subject = f'Message from {sender}, {sender_email}'
        
        mail_admins(subject, message, fail_silently=False)

        return render(self.request, 'contact_message.html')


class CustomerAccountView(TemplateView):
    model = Customer
    template_name = 'customer_account.html'


class CustomerCreateView(FormView):
    model = Customer
    form_class = CustomerCreateForm
    template_name = 'customer_create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        phone = form.cleaned_data['phone']
        address = form.cleaned_data['address']

        permission = Permission.objects.get(name='Can change user')

        customer = Customer.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone=phone,
            address=address
        )

        customer.set_password(password)
        customer.user_permissions.add(permission)
        customer.save()

        Cart.objects.create(owner = customer)

        subject = 'Welcome to AntShop'
        message = f'''
            {customer.full_name}, welcome to AntShop! 
            Hope you are enjoying shopping here.
            Let's start https://ant-shop.herokuapp.com/
        '''
        recepient = str(form['email'].value())
        send_mail(
            subject, 
            message, 
            EMAIL_HOST_USER, 
            [recepient], 
            fail_silently = False
        )

        return HttpResponseRedirect(self.get_success_url())


class CustomerDataUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = CustomerUpdateForm
    permission_required = 'products.change_customer'
    template_name = 'customer_data_update.html'
    success_message = 'Your personal data has been successfully changed!'
    success_url = reverse_lazy('customer_account')
    

class CustomerPasswordUpdateView(PermissionRequiredMixin, PasswordChangeView):
    template_name = 'customer_change_password.html'
    success_url = reverse_lazy('customer_account')
    permission_required = 'products.change_customer'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

