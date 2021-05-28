from products.models import Category, Customer, Product, Subcategory
from products.views import get_customer_cart


def base_page_info(request):
    ctx = {
        'admin': Customer.objects.get(username='admin'),
        'cart': get_customer_cart(request),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'products': Product.objects.order_by('-creation_date')[:9],
    }
    return ctx
