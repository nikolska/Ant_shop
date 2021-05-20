from django.urls import path, re_path

from .views import HomePageView, ProductDetailView, ProductListView


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
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
