from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='categories/')

    def get_absolute_url(self):
        return reverse('category', args=[str(self.pk)])

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'


class Subcategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('product_list', args=[str(self.pk)])

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Subcategories'


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    code = models.CharField(max_length=255, unique=True)
    rating = models.FloatField(default=1.0)
    availability = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
    

    class Meta:
        ordering = ['name']
