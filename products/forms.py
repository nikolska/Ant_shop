import re
from datetime import datetime, timedelta

from django import forms

from .models import Comment, Customer, Order


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text', 'rating']
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['rating'] < 1 or cleaned_data['rating'] > 10:
            self.add_error('rating', 'Please, select a rating from 1.0 to 10!')


class ContactForm(forms.Form):
    sender = forms.CharField(
        label="Your Full Name", 
        max_length=255, 
        widget=forms.TextInput({'class': 'form-control contact-form', 'placeholder': 'Your name'})
    )
    sender_email = forms.EmailField(
        label="Email Address", 
        widget=forms.EmailInput({'class': 'form-control contact-form', 'placeholder': 'Email address'})
    )
    message_text = forms.CharField(
        label="Message Text", 
        widget=forms.Textarea({'class': 'form-control contact-form', 'placeholder': 'Message text', 'rows': 5})
    )


class CustomerCreateForm(forms.ModelForm):
    repeat_password = forms.CharField(widget=forms.PasswordInput({'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'phone', 'address', 'password', 'repeat_password'
        ]
        widgets = {
            'first_name': forms.TextInput({'class': 'form-control'}),
            'last_name': forms.TextInput({'class': 'form-control'}),
            'username': forms.TextInput({'class': 'form-control'}),
            'email': forms.EmailInput({'class': 'form-control'}),
            'phone': forms.TextInput({'class': 'form-control'}),
            'address': forms.TextInput({'class': 'form-control'}),
            'password': forms.PasswordInput({'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['repeat_password']:
            self.add_error('password', 'Passwords do not match!')
        if Customer.objects.filter(username=cleaned_data['username']):
            self.add_error('username', 'This username is already taken, try another one.')
        if not re.fullmatch(r'^\+\d+$', cleaned_data['phone']):
            self.add_error('phone', 'Start with + . Then digits only!')


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput({'class': 'form-control'}),
            'last_name': forms.TextInput({'class': 'form-control'}),
            'username': forms.TextInput({'class': 'form-control'}),
            'email': forms.EmailInput({'class': 'form-control'}),
            'phone': forms.TextInput({'class': 'form-control'}),
            'address': forms.TextInput({'class': 'form-control'}),
        }


class InformForm(forms.Form):
    email = forms.EmailField(
        label="Email Address", 
        widget=forms.EmailInput({'class': 'form-control', 'placeholder': 'Email address'})
    )


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Date of receipt of the order (at least 2 working days, excluding weekends and holidays)'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'email', 'phone', 
            'address', 'buying_type', 'order_date', 'comment'
        )
        labels = {
            'phone': 'Phone (start with +)'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        if not re.fullmatch(r'^\+\d+$', cleaned_data['phone']):
            self.add_error('phone', 'Start with + . Then digits only!')
        if cleaned_data['order_date'] < (datetime.today().date() + timedelta(days=2)) or cleaned_data['order_date'].weekday() > 4:
            self.add_error('order_date', 'Please, check the correct date!')

