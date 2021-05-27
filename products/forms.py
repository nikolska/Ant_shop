import re

from django import forms

from .models import Customer


class ContactForm(forms.Form):
    sender = forms.CharField(
        label="Your Full Name", 
        max_length=255, 
        widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Your full name'})
    )
    sender_email = forms.EmailField(
        label="Email Address", 
        widget=forms.EmailInput({'class': 'form-control', 'placeholder': 'Your contact email'})
    )
    message_text = forms.CharField(
        label="Message Text", 
        widget=forms.Textarea({'class': 'form-control', 'placeholder': 'Message text'})
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
