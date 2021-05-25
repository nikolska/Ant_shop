from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import mail_admins, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView, UpdateView

from .forms import ContactForm, CustomerCreateForm, CustomerUpdateForm, LoginForm
from .models import Cart, Category, Customer, Product, Subcategory
from ant_shop.settings import EMAIL_HOST_USER


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


# class LoginView(LoginView):
#     form_class = LoginForm
#     template_name = 'login.html'

