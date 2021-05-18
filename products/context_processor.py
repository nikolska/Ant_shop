from django.shortcuts import get_list_or_404

from .models import Cart, Category, Customer, LatestProducts, Subcategory


def base_page_info(request):
    customer = Customer.objects.get(user=request.user)
    ctx = {
        'cart': Cart.objects.get(owner=customer, in_order=False),
        'categories': get_list_or_404(Category),
        'subcategories': get_list_or_404(Subcategory),
        'products': LatestProducts.objects.get_products_for_main_page('ant', 'formicary'),
    }
    return ctx
