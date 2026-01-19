from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SimpleRegistrationForm(forms.Form):
    """Simple registration form with minimal password validation"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'At least 8 characters'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter password'})
    )
    age = forms.IntegerField(
        min_value=5,
        max_value=18,
        initial=8,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    grade_level = forms.ChoiceField(
        choices=[
            ('Kindergarten', 'Kindergarten'),
            ('1st', '1st Grade'),
            ('2nd', '2nd Grade'),
            ('3rd', '3rd Grade'),
            ('4th', '4th Grade'),
            ('5th', '5th Grade'),
            ('6th', '6th Grade'),
            ('7th', '7th Grade'),
            ('8th', '8th Grade'),
            ('9th', '9th Grade'),
            ('10th', '10th Grade'),
            ('11th', '11th Grade'),
            ('12th', '12th Grade'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken. Please choose another one.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')

        return cleaned_data

    def save(self):
        """Create and return a new user"""
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1']
        )
        return user
