from django.contrib.auth.views import (
    LoginView , LogoutView, PasswordResetCompleteView, 
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
)
from django.urls import path, re_path

from .views import (
    AddToCartView, CartView, ContactView, CustomerAccountView, 
    CustomerCreateView, CustomerDataUpdateView, CustomerPasswordUpdateView, 
    HomePageView, ProductDetailView, ProductListView
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
    path('contact-us/', ContactView.as_view(), name='contact'),
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
