from django.shortcuts import get_list_or_404

from products.models import Category, Product, Subcategory


def base_page_info(request):
    ctx = {
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'products': Product.objects.all(),
    }
    return ctx
