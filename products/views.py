from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import mail_admins, send_mail
from django.db import models, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView, UpdateView, View

from .forms import CommentForm, ContactForm, CustomerCreateForm, CustomerUpdateForm, InformForm, OrderForm
from .models import Cart, CartProduct, Category, Comment, Customer, Order, Product, Subcategory, Wish_List
from ant_shop.settings import EMAIL_HOST_USER


def get_customer_cart(request):
    if request.user.is_anonymous:
        cart = Cart.objects.filter(for_anonymous_user=True, in_order=False).first()
        if not cart:
            cart = Cart.objects.create(for_anonymous_user=True)
    else:
        customer = Customer.objects.get(username=request.user.username)
        cart = Cart.objects.filter(owner=customer, in_order=False).first()
        if not cart:
            cart = Cart.objects.create(owner=customer)
    return cart


def get_customer_wishlist(request):
    if request.user.is_anonymous:
        wishlist = Wish_List.objects.filter(for_anonymous_user=True).first()
        if not wishlist:
            wishlist = Wish_List.objects.create(for_anonymous_user=True)
    else:
        customer = Customer.objects.get(username=request.user.username)
        wishlist = Wish_List.objects.get(owner=customer)
        if not wishlist:
            wishlist = Wish_List.objects.create(owner=customer)
    return wishlist


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Sum('qty'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.total_products = cart_data['qty__sum']
    cart.save()


def recalc_wishlist(wishlist):
    wishlist_data = wishlist.products.aggregate(models.Count('id'))
    wishlist.total_products = wishlist_data['id__count']
    wishlist.save()


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        cart = get_customer_cart(request)
        product = Product.objects.get(slug=kwargs.get('slug'))
        cart_product, created = CartProduct.objects.get_or_create(
            product=product,
            customer=cart.owner,
            cart=cart,
            final_price=product.price
        )
        if created:
            cart.products.add(cart_product)
        recalc_cart(cart)
        messages.add_message(request, messages.INFO, f'{product.title} added to cart')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddToWishListView(View):
    def get(self, request, *args, **kwargs):
        wishlist = get_customer_wishlist(request)
        product = Product.objects.get(slug=kwargs.get('slug'))
        wishlist.products.add(product)
        recalc_wishlist(wishlist)
        messages.add_message(request, messages.INFO, f'{product.title} added to wish list')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CartView(View):
    def get(self, request, *args, **kwargs):
        cart = get_customer_cart(request)
        ctx = {'cart': cart}
        return render(request, 'cart_view.html', ctx)


class ChangeProductQuantityView(View):
    def post(self, request, *args, **kwargs):
        cart = get_customer_cart(request)
        product = Product.objects.get(slug=kwargs.get('slug'))
        cart_product = CartProduct.objects.get(
            product=product,
            customer=cart.owner,
            cart=cart
        )
        product_quantity = int(request.POST.get('product_quantity'))
        cart_product.qty = product_quantity
        cart_product.save()
        recalc_cart(cart)
        messages.add_message(request, messages.INFO, f'Quantity of {product.title} changed')
        return HttpResponseRedirect('/cart/')


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

        Cart.objects.create(owner=customer)
        Wish_List.objects.create(owner=customer)

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


class CustomerDataUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = CustomerUpdateForm
    permission_required = 'products.change_customer'
    template_name = 'customer_data_update.html'
    success_message = 'Your personal data has been successfully changed!'
    success_url = reverse_lazy('customer_account')
    

class CustomerOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'customer_orders.html'

    def dispatch(self, request, *args, **kwargs):
        self.queryset = self.model.objects.filter(customer=request.user).order_by('-order_date')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        dictionary = {}
        for key, value in self.request.session.items():
            if key.isdigit():
                dictionary[int(key)] = value
        ctx['dictionary'] = dictionary
        return ctx


class CustomerPasswordUpdateView(LoginRequiredMixin, PermissionRequiredMixin, PasswordChangeView):
    template_name = 'customer_change_password.html'
    success_url = reverse_lazy('customer_account')
    permission_required = 'products.change_customer'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DeleteFromCartView(View):
    def get(self, request, *args, **kwargs):
        cart = get_customer_cart(request)
        product = Product.objects.get(slug=kwargs.get('slug'))
        cart_product = CartProduct.objects.get(
            product=product,
            customer=cart.owner,
            cart=cart
        )
        cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(cart)
        messages.add_message(request, messages.INFO, f'{product.title} removed from cart')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteFromWishListView(View):
    def get(self, request, *args, **kwargs):
        wishlist = get_customer_wishlist(request)
        product = Product.objects.get(slug=kwargs.get('slug'))
        wishlist.products.remove(product)
        recalc_wishlist(wishlist)
        messages.add_message(request, messages.INFO, f'{product.title} removed from wish list')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class HomePageView(TemplateView):
    template_name = 'home_page.html'


class InformCustomerView(FormView):
    form_class = InformForm
    template_name = 'inform_customer.html'
    
    def form_valid(self, form, *args, **kwargs):
        
        product = Product.objects.get(slug=self.kwargs['slug'])
        email = form.cleaned_data['email']

        subject = f"Message from AntShop customer to inform about {product} avalibility"
        message = f'''
            Hello, I'm your customer from AntShop WebSite. Please, inform me {email} about 
            https://ant-shop.herokuapp.com/products/{product.get_absolute_url()} {product} avalibility.
        '''

        mail_admins(subject, message, fail_silently=False)

        return render(self.request, 'contact_message.html')


class MakeOrderView(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = request.user
        cart = get_customer_cart(request)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.email = form.cleaned_data['email']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            
            if not request.user.is_anonymous:
                new_order.customer = customer

            new_order.save()

            order_final_price = cart.final_price
            if new_order.buying_type == 'BUYING_TYPE_DELIVERY':
                order_final_price += Order.DELIVERY_COST

            products = []
            for item in cart.products.all():
                products.append(item.product.title)
                item.product.qty -= item.qty
                item.product.save()

            cart.in_order = True
            cart.save()
            new_order.cart = cart
            new_order.save()
            
            if not request.user.is_anonymous:
                customer.related_orders.add(new_order)

            subject_for_admin = f'Some customer of your AntShop bought your product'
            message_for_admin = f'''
                Customer details:
                First name: {new_order.first_name}
                Last name: {new_order.last_name}
                Email: {new_order.email}
                Phone: {new_order.phone}
                Address: {new_order.address}
                Order details:
                Products ({cart.total_products}): {products}
                Total price: {order_final_price}
                Buying type: {new_order.buying_type}
                Order date: {new_order.order_date}
                Comment: {new_order.comment}
            '''

            mail_admins(subject_for_admin, message_for_admin, fail_silently=False)

            subject_for_customer = 'Thank you for the order in AntShop!'
            message_for_customer = f'''
                {new_order.first_name} {new_order.last_name}, 
                thank you for shopping in AntShop! 
                You buy {cart.total_products} products: {products}
                Total price: {order_final_price}
                Order details:
                First name: {new_order.first_name}
                Last name: {new_order.last_name}
                Email: {new_order.email}
                Phone: {new_order.phone}
                Address: {new_order.address}
                Buying type: {new_order.buying_type}
                Order date: {new_order.order_date}
                Comment: {new_order.comment}
                You can check you order's details in you personal account 
                https://ant-shop.herokuapp.com/account/
            '''

            send_mail(
                subject_for_customer, 
                message_for_customer, 
                EMAIL_HOST_USER, 
                [new_order.email], 
                fail_silently = False
            )

            messages.add_message(request, messages.INFO, '''
                Thank you for the order! Check your email address for a letter with all the details of this order. 
                You can also see them in your personal account in the <a href="/account/orders/">ORDERS</a> section.
            ''')
            return HttpResponseRedirect('/')
        messages.add_message(request, messages.ERROR, '''
            Please, enter a valid data! <br>
            Email must contains @ and server domain name. <br>
            Phone number must start with + and then only digits. <br>
            Date should be at least 2 working days, excluding weekends and holidays.
        ''')
        return HttpResponseRedirect('/order/')


class OrderView(FormView):
    form_class = OrderForm
    template_name = 'order_form.html'


class ProductDetailView(DetailView, FormView):
    model = Product
    form_class = CommentForm
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        comments = Comment.objects.filter(product=self.object)
        related_products = Product.objects.filter(category=self.object.category).exclude(slug=self.object.slug)[:3]
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = comments
        ctx['related_products'] = related_products
        return ctx

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment_text']
            rating = form.cleaned_data['rating']

            if not self.request.user.is_anonymous:    
                Comment.objects.create(
                    product=self.get_object(), author=self.request.user,
                    comment_text=comment_text, rating=rating
                )
            else:
                Comment.objects.create(product=self.get_object(), comment_text=comment_text, rating=rating)

            self.object = self.get_object()
            ctx = self.get_context_data(**kwargs)
            ctx['form'] = form
            return self.render_to_response(context=ctx)
        else:
            self.object = self.get_object()
            ctx = self.get_context_data(**kwargs)
            ctx['form'] = form
            return self.render_to_response(context=ctx)


class ProductListView(ListView):
    model = Product
    paginate_by = 30
    template_name = 'product_list.html'
    slug_url_kwarg = 'slug'

    def get_subcategory_list(self, category_slug):
        category = Category.objects.get(slug=category_slug)
        subcategory_list = Subcategory.objects.filter(category=category)
        return subcategory_list

    def dispatch(self, request, *args, **kwargs):
        subcategory_list = self.get_subcategory_list(kwargs['category'])
        self.queryset = self.model.objects.filter(category__in=subcategory_list)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        subcategory_list = self.get_subcategory_list(self.kwargs['category'])
        ctx = super().get_context_data(**kwargs)
        ctx['subcategory_list'] = subcategory_list
        return ctx
    
    def get_queryset(self):
        if self.request.GET.get('category_sorting'):
            sort = self.request.GET.get('category_sorting')
            category = Subcategory.objects.get(name=sort)
            queryset = self.model.objects.filter(category=category)  
            return queryset

        product_sorting = self.request.GET.get('sorting')
        
        if product_sorting == '1':
            queryset = self.queryset.order_by('-rating')
            return queryset
        elif product_sorting == '2':
            queryset = self.queryset.order_by('price')
            return queryset
        elif product_sorting == '3':
            queryset = self.queryset.order_by('-price')
            return queryset
        elif product_sorting == '4':
            queryset = self.queryset.order_by('-creation_date')
            return queryset

        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        rating_from = self.request.GET.get('rating_from')
        rating_to = self.request.GET.get('rating_to')
        avalible = self.request.GET.get('availability')

        max_price = Product.objects.aggregate(models.Max('price'))
        
        price_from = Decimal(price_from) if price_from else 0.0
        price_to = Decimal(price_to) if price_to else max_price.get('price__max')
        rating_from = float(rating_from) if rating_from else 0
        rating_to = float(rating_to) if rating_to else 10
        
        queryset = self.queryset.filter(
                price__range=(price_from, price_to),
                rating__range=(rating_from, rating_to),
            )

        if avalible == '1':
            queryset = self.queryset.filter(availability=True)
        elif avalible == '2':
            queryset = self.queryset.filter(availability=False)
        
        if self.request.GET.get('reset_f') or self.request.GET.get('reset_s'):
            return self.queryset

        return queryset


class ProductSearchView(View):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            products = Product.objects.filter(title__icontains=search)
            ctx = {'products': products}
            return render(request, 'product_search.html', ctx)


class RateProductView(View):
    def post(self, request, *args, **kwargs):
        customer_rating = request.POST.get('customer_rating')
        product = Product.objects.get(slug=kwargs.get('slug'))
        new_rating = round((product.rating + float(customer_rating)) / 2, 1)
        product.rating = new_rating
        request.session[f'{product.pk}'] = customer_rating
        product.save()
        messages.add_message(request, messages.INFO, 
            f'Thank you for rate {product.title}! Your rating for this product is {customer_rating}.'
        )
        
        return HttpResponseRedirect('/account/orders/')
        

class WishListView(View):
    def get(self, request, *args, **kwargs):
        wishlist = get_customer_wishlist(request)
        ctx = {'wishlist': wishlist}
        return render(request, 'wishlist_view.html', ctx)
