from PIL import Image

from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.utils.safestring import mark_safe

from .models import Cart, CartProduct, Category, Customer, Order, Product, Subcategory


class CartAdmin(admin.ModelAdmin):
    list_display = ('owner', 'total_products', 'final_price', 'in_order', 'for_anonymous_user')
    list_filter = ('owner', 'in_order', 'for_anonymous_user')
    search_fields = ('owner',)


class CartProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'cart', 'qty', 'final_price', 'get_small_image')
    list_filter = ('product', 'customer', 'cart')
    search_fields = ('product',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.product.image.url} width="250" height="150">')
    
    def get_small_image(self, obj):
        return mark_safe(f'<img src={obj.product.image.url} width="130" height="70">')
    
    get_image.short_description = 'Preview'
    get_small_image.short_description = 'Image'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


class CustomerAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone'].help_text = mark_safe('''
            <span style="color: grey">
               Start from + . Then digits only
            </span>
        ''')
        self.fields['address'].help_text = mark_safe('''
            <span style="color: grey">
                Street name and number, Apartment/Room, City/Town/Village, Postal code, Country
            </span>
        ''')


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm
    list_display = ('full_name', 'username', 'email', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('full_name', 'first_name', 'last_name', 'email', 'phone', 'address')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'cart', 'email', 'status', 'buying_type', 'created_at', 'order_date')
    list_filter = ('status', 'buying_type', 'created_at', 'order_date')
    search_fields = ('customer', 'first_name', 'last_name', 'email', 'phone', 'address')


class ProductCategoryFilter(admin.SimpleListFilter):
    title = 'main category'
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


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


admin.site.register(Cart, CartAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
