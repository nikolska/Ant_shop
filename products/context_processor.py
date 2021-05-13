from django.shortcuts import get_list_or_404

from .models import Ant, Category, Formicary, Product


def base_page_info(request):
    ctx = {
        'categories': get_list_or_404(Category),
        'products': get_list_or_404(Ant) + get_list_or_404(Formicary),
    }
    return ctx
