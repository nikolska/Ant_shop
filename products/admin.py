from PIL import Image

from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.utils.safestring import mark_safe

from .models import Cart, Category, Customer, Product, Specification, Subcategory


class ProductAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
    form = ProductAdminForm
    list_display = ('title', 'category', 'price', 'code', 'availability')
    list_filter = ('availability', 'category')
    search_fields = ('title',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="200" height="150">')
    
    get_image.short_description = 'Preview'


admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Specification)
admin.site.register(Subcategory)
