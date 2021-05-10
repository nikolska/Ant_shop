from django import forms
from django.contrib import admin

from .models import Ant, Cart, CartProduct, Category, Customer, Formicary, Subcategory


class AntCategoryChoiceField(forms.ModelChoiceField):
    pass


class AntAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return AntCategoryChoiceField(Subcategory.objects.filter(slug__contains='ants'))
        return super().formfiled_for_foreignkey(db_field, request, **kwargs)


class FormicaryCategoryChoiceField(forms.ModelChoiceField):
    pass


class FormicaryAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return FormicaryCategoryChoiceField(Subcategory.objects.filter(slug__contains='formicaries'))
        return super().formfiled_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Ant, AntAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Formicary, FormicaryAdmin)
admin.site.register(Subcategory)
