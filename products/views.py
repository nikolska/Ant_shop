from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView, UpdateView

from .forms import CustomerCreateForm, CustomerUpdateForm
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


class CustomerDataUpdateView(PermissionRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerUpdateForm
    template_name = 'customer_data_update.html'
    success_url = reverse_lazy('customer_account')
    permission_required = 'products.change_customer'


# class CustomerPasswordResetView(PermissionRequiredMixin, PasswordResetView):
#     email_template_name = 'registration/password_reset_email.html'
#     # form_class = PasswordResetForm
#     from_email = EMAIL_HOST_USER
#     subject_template_name = 'registration/password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')
#     template_name = 'registration/password_reset_form.html'
#     # title = 'Password reset'

#     # template_name = 'customer_change_password.html'
#     # success_url = reverse_lazy('customer_account')
#     # permission_required = 'products.change_customer'

#     # def form_valid(self, form):
#     #     form.save()
#     #     return super().form_valid(form)


class CustomerPasswordUpdateView(PermissionRequiredMixin, PasswordChangeView):
    template_name = 'customer_change_password.html'
    success_url = reverse_lazy('customer_account')
    permission_required = 'products.change_customer'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

