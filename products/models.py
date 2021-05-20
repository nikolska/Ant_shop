from PIL import Image

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

User = get_user_model()


def get_product_url(object, viewname):
    return reverse(viewname, kwargs={
        'category': object.category.category.slug,
        'subcategory': object.category.slug,
        'slug': object.slug
    })


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return f'{self.full_name}'


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


class Specification(models.Model):
    size = models.CharField(max_length=100, blank=True)
    coloration = models.CharField(max_length=100, blank=True)
    occurrence = models.CharField(max_length=255, blank=True)
    nesting = models.CharField(max_length=255, blank=True)
    dimensions = models.CharField(max_length=255, blank=True)
    material = models.CharField(max_length=100, blank=True)
    additional_info = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.pk}'


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=255, unique=True)
    rating = models.FloatField(default=1.0, validators=[MinValueValidator(0.0), MaxValueValidator(10)])
    availability = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/')
    creation_date = models.DateField(auto_now=True)

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
        ordering = ['title']
    
    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Cart(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=True)
    products = models.ManyToManyField(Product, blank=True)
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
            return f'Cart of {self.owner}'

