from django.urls import path, re_path

from .views import HomePageView, ProductDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    re_path(
        r'^products/(?P<ct_model>\w+-?\w+-?\w+-?\w+)/(?P<category>\w+-?\w+-?\w+-?\w+)/(?P<slug>\w+-?\w+-?\w-?\w+-?\w+-?\w+)/$', 
        ProductDetailView.as_view(), 
        name='product_detail'
    ),
]