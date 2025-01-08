# authentication/forms.py
from django import forms # login form-hoz

from django.contrib.auth import get_user_model #singup form-hoz
from django.contrib.auth.forms import UserCreationForm #singup form-hoz

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name')