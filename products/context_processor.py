from django.shortcuts import get_list_or_404

from .models import Category, Product, Subcategory


def base_page_info(request):
    ctx = {
        'categories': get_list_or_404(Category),
        'subcategories': get_list_or_404(Subcategory),
        'products': get_list_or_404(Product),
    }
    return ctx
