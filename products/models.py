from PIL import Image
import string

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


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


class Customer(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
    
    def save(self, *args, **kwargs):
        self.name = string.capwords(self.name)
        super().save(*args, **kwargs)


class Subcategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Subcategories'
    
    def save(self, *args, **kwargs):
        self.name = string.capwords(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    code = models.CharField(max_length=255, unique=True)
    rating = models.FloatField(default=1.0, validators=[MinValueValidator(0.0), MaxValueValidator(10)])
    availability = models.BooleanField(default=False)
    qty = models.PositiveIntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    creation_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.title = string.capwords(self.title)
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


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='related_products')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return f'Cart of {self.owner}'


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'New order'),
        (STATUS_IN_PROGRESS, 'Order in progress'),
        (STATUS_READY, 'Order is ready'),
        (STATUS_COMPLETED, 'Order completed')
    )

    DELIVERY_COST = 7

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Self-pickup'),
        (BUYING_TYPE_DELIVERY, f'Delivery ({DELIVERY_COST}$)')
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='related_orders', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(max_length=100, choices=BUYING_TYPE_CHOICES)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    order_date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.id)


class Wish_List(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    total_products = models.PositiveIntegerField(default=0)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} wish list'

