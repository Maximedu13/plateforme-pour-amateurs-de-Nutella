from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    user = forms.CharField(max_length=100)
    mdp = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    user = forms.CharField(max_length=100)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    checkbox = forms.BooleanField(required=True)