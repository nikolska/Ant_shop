from PIL import Image

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.urls import reverse


User = get_user_model()


class MinResolutionErrorException(Exception):
    pass

class MaxResolutionErrorException(Exception):
    pass


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)

        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)

        if with_respect_to:
            ct_model = ContentType.objects.filter(model__in=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True)
        
        return products


class LatestProducts:
    objects = LatestProductsManager()


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.full_name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'


class Subcategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Subcategories'


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    code = models.CharField(max_length=255, unique=True)
    rating = models.FloatField(default=1.0)
    availability = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_height, min_width = (400, 400)
        max_height, max_width = (2000, 2000)
        
        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorException('The resolution of image is too small')
        
        if img.height > max_height or img.width > max_width:
            raise MaxResolutionErrorException('The resolution of image is too big')
        
        super().save(*args, **kwargs)
    

    class Meta:
        abstract = True


class CartProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    card = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object_id = GenericForeignKey('content_type', 'object_id')
    count = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2)
    
    def __str__(self):
            return f'{self.product.title} (for Cart)'
        

class Cart(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
            return f'{self.owner.user.full_name} Cart'


class Ant(Product):
    size = models.CharField(max_length=100)
    coloration = models.CharField(max_length=100)
    occurrence = models.CharField(max_length=255)
    nesting = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']


class Formicary(Product):
    dimensions = models.CharField(max_length=255)
    formicary_material = models.CharField(max_length=100)
    additional_info = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Formicaries'

