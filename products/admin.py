from PIL import Image

from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe

from .models import Ant, Cart, CartProduct, Category, Customer, Formicary, Subcategory


class AntsCategoryFilter(admin.SimpleListFilter):
    title = 'category'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        categories = Subcategory.objects.filter(slug__contains='ants')
        return [(category.id, category.name) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id__exact=self.value())
        else:
            return queryset


class FormicariesCategoryFilter(admin.SimpleListFilter):
    title = 'category'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        categories = Subcategory.objects.filter(slug__contains='formicaries')
        return [(category.id, category.name) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id__exact=self.value())
        else:
            return queryset


class ProductAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe('''
            <span style="color: red">
                Minimum resolution for images: 400x400
            </span>
        ''')

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = (400, 400)
        max_height, max_width = (2000, 2000)

        if img.height < min_height or img.width < min_width:
            raise ValidationError('The resolution of image is too small')
        
        if img.height > max_height or img.width > max_width:
            raise ValidationError('The resolution of image is too big')

        return image


class AntAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('title', 'category', 'price', 'code', 'availability')
    list_filter = ('availability', AntsCategoryFilter)
    search_fields = ('title',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="150">')
    
    get_image.short_description = 'Image'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Subcategory.objects.filter(slug__contains='ants'))
        return super().formfiled_for_foreignkey(db_field, request, **kwargs)


class FormicaryAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('title', 'category', 'price', 'code', 'availability')
    list_filter = ('availability', FormicariesCategoryFilter)
    search_fields = ('title',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="150">')

    get_image.short_description = 'Image'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Subcategory.objects.filter(slug__contains='formicaries'))
        return super().formfiled_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Ant, AntAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Formicary, FormicaryAdmin)
admin.site.register(Subcategory)
