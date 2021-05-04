from django import forms

from .models import Category, Product, Subcategory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        labels = {
            'name': 'Category name',
            'image': 'Category image'
        }


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name']
        labels = {'name': 'Subcategory name'}

