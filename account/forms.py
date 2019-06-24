"""forms which manage the accounts"""
from django import forms

class LoginForm(forms.Form):
    """the form to login"""
    user = forms.CharField(max_length=100)
    mdp = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    """the form to create an account"""
    user_name = forms.CharField(max_length=100)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    checkbox = forms.BooleanField(required=True)
