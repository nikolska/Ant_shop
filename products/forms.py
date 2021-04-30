from django import forms

from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category()
        fields = ['name', 'description', 'image']
        labels = {
            'name': 'Category name', 
            'description': 'Description', 
            'image': 'Image'
        }
