from products.forms import ProductFilterForm, ProductSearchForm, ProductSortForm
from products.models import Category, Customer, Product, Subcategory
from products.views import get_customer_cart, get_customer_wishlist


def base_page_info(request):
    ctx = {
        'admin': Customer.objects.get(username='admin'),
        'cart': get_customer_cart(request),
        'categories': Category.objects.all(),
        'products': Product.objects.order_by('-creation_date')[:9],
        'filter_form': ProductFilterForm,
        'search_form': ProductSearchForm,
        'sort_form': ProductSortForm,
        'subcategories': Subcategory.objects.all(),
        'wishlist': get_customer_wishlist(request),
    }
    return ctx
