from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


User = get_user_model()


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.full_name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('category', args=[str(self.pk)])

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'


class Subcategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('product_list', args=[str(self.pk)])

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
    

    class Meta:
        ordering = ['title']


class CartProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    card = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
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


class Specification(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product_title = models.CharField(max_length=255)

    def __str__(self):
            return f'Specification for {self.product_title}'

