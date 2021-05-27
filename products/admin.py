from PIL import Image

from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.utils.safestring import mark_safe

from .models import Cart, CartProduct, Category, Customer, Product, Subcategory


class ProductCategoryFilter(admin.SimpleListFilter):
    title = ' main category'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        categories = Category.objects.all()
        return [(category.id, category.name) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id__exact=self.value())
        else:
            return queryset


class ProductAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and not instance.availability:
            self.fields['qty'].widget.attrs.update({
                'readonly': True, 'style': 'background: lightgray;'
            })

        self.fields['slug'].help_text = mark_safe('''
            <span style="color: red">
                The field can only contain letters, numbers, underscores or hyphens
            </span>
        ''')
        self.fields['image'].help_text = mark_safe('''
            <span style="color: red">
                Minimum resolution for images: 400x400
            </span>
        ''')
        self.fields['rating'].help_text = mark_safe('''
            <span style="color: red">
                Choose from 0 to 10
            </span>
        ''')

    def clean(self):
        if not self.cleaned_data['availability']:
            self.cleaned_data['qty'] = None
        return self.cleaned_data

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


class ProductAdmin(admin.ModelAdmin):
    change_form_template = 'admin.html'
    form = ProductAdminForm
    list_display = ('title', 'category', 'price', 'code', 'availability', 'qty', 'get_small_image')
    list_filter = ('availability', ProductCategoryFilter, 'category')
    search_fields = ('title',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="250" height="150">')
    
    def get_small_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="130" height="70">')
    
    get_image.short_description = 'Preview'
    get_small_image.short_description = 'Image'


admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subcategory)
