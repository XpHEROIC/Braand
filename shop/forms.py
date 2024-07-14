from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Customer, ShippingAddress, Profile


# Form for login
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input',
    }))
    class Meta:
        model = User
        fields = ('username', 'password')


# Form for registrations
class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input',
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input',
    }))

    number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'contact__section-input',
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'number', 'password1', 'password2')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'contact__section-input'}),
            'email': forms.EmailInput(attrs={'class': 'contact__section-input'}),
            'text': forms.Textarea(attrs={'class': 'contact__section-input'}),
        }


# Form for Customer
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя...'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше фамилия...'
            })

        }


# Forms for delevery
class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'region', 'phone']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше адрес...'
            }),

            'city': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Ваше город...'
            }),

            'region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше регион...'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше телефон...'
            }),

        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'last_name', 'city', 'street', 'house', 'email', 'number']



