from django.contrib.auth.views import (
    LoginView , LogoutView, PasswordResetCompleteView, 
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
)
from django.urls import path, re_path

from .views import (
    AddToCartView, CartView, ChangeProductQuantityView, ContactView, 
    CustomerAccountView, CustomerCreateView, CustomerDataUpdateView, 
    CustomerPasswordUpdateView, DeleteFromCartView, HomePageView, 
    InformCustomerView, MakeOrderView, OrderView, ProductDetailView, ProductListView
)


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('account/', CustomerAccountView.as_view(), name='customer_account'),
    path('account/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('account/logout/', LogoutView.as_view(), name='logout'),
    path('account/registration/', CustomerCreateView.as_view(), name='registration'),
    re_path(r'^account/reset-password/$', PasswordResetView.as_view(), name='password_reset'),
    re_path(r'^account/reset-password/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(
        r'^account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'
    ),
    re_path(r'^account/reset/done/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    re_path(r'^account/update-password/(?P<pk>\d+)/$', CustomerPasswordUpdateView.as_view(), name='update_customer_password'),
    re_path(r'^account/update-personal-data/(?P<pk>\d+)/$', CustomerDataUpdateView.as_view(), name='update_customer_data'),
    re_path(r'^add-to-cart/(?P<slug>[-\w]+)/$', AddToCartView.as_view(), name='add_to_cart'),
    re_path(r'^cart/$', CartView.as_view(), name='cart_view'),
    re_path(r'^change-cart-products-quantity/(?P<slug>[-\w]+)/$', ChangeProductQuantityView.as_view(), name='change_product_quantity'),
    re_path(r'^contact-us/$', ContactView.as_view(), name='contact'),
    re_path(r'^inform-me/(?P<slug>[-\w]+)/$', InformCustomerView.as_view(), name='inform_customer'),
    re_path(r'^make-order/$', MakeOrderView.as_view(), name='make_order'),
    re_path(r'^order/$', OrderView.as_view(), name='order_form'),
    re_path(r'^remove-from-cart/(?P<slug>[-\w]+)/$', DeleteFromCartView.as_view(), name='delete_from_cart'),
    re_path(
        r'^products/(?P<category>[-\w]+)/(?P<subcategory>[-\w]+)/(?P<slug>[-\w]+)/$', 
        ProductDetailView.as_view(), 
        name='product_detail'
    ), 
    re_path(
        r'^products/(?P<category>[-\w]+)/(?P<subcategory>[-\w]+)/$', 
        ProductListView.as_view(), 
        name='product_list'
    ),
]
