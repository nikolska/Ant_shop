from django.contrib import admin

from .models import Category, Product, Subcategory


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Subcategory)
