from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path, re_path

from .views import CustomerAccountView, CustomerCreateView, HomePageView, ProductDetailView, ProductListView


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('account/', CustomerAccountView.as_view(), name='user_account'),
    path('account/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('account/logout/', LogoutView.as_view(), name='logout'),
    path('account/registration/', CustomerCreateView.as_view(), name='registration'),
    re_path(
        r'^products/(?P<category>\w+-?\w+-?\w+-?\w+)/(?P<subcategory>\w+-?\w+-?\w+-?\w+)/(?P<slug>\w+-?\w+-?\w-?\w+-?\w+-?\w+)/$', 
        ProductDetailView.as_view(), 
        name='product_detail'
    ), 
    re_path(
        r'^products/(?P<category>\w+-?\w+-?\w+-?\w+)/(?P<subcategory>\w+-?\w+-?\w+-?\w+)/$', 
        ProductListView.as_view(), 
        name='product_list'
    ),
]
