from django import forms

from .models import Customer


class CustomerCreateForm(forms.ModelForm):
    """Create new user form."""
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        """Meta class."""
        model = Customer
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'phone', 'address', 'password', 'repeat_password'
        ]
        widgets = {
            'password': forms.PasswordInput,
            'repeat_password': forms.PasswordInput
        }

    def clean(self):
        """Method to validate the password."""
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['repeat_password']:
            self.add_error('password', 'Passwords do not match!')
        if Customer.objects.filter(username=cleaned_data['username']):
            self.add_error('username', 'This username is already taken, try another one!')

