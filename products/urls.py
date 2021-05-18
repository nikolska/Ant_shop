from django.urls import path, re_path

from .views import AddToCartView, CartView, HomePageView, ProductDetailView, ProductListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    re_path(
        r'^add-to-cart/(?P<ct_model>\w+-?\w+-?\w+-?\w+)/(?P<category>\w+-?\w+-?\w+-?\w+)/(?P<slug>\w+-?\w+-?\w-?\w+-?\w+-?\w+)/$', 
        AddToCartView.as_view(), 
        name='add_to_cart'),
    re_path(r'^cart/$', CartView.as_view(), name='cart_view'),
    re_path(
        r'^products/(?P<ct_model>\w+-?\w+-?\w+-?\w+)/(?P<category>\w+-?\w+-?\w+-?\w+)/(?P<slug>\w+-?\w+-?\w-?\w+-?\w+-?\w+)/$', 
        ProductDetailView.as_view(), 
        name='product_detail'
    ),  
    re_path(
        r'^products/(?P<ct_model>\w+-?\w+-?\w+-?\w+)/(?P<category>\w+-?\w+-?\w+-?\w+)/$', 
        ProductListView.as_view(), 
        name='product_list'
    ),
]
