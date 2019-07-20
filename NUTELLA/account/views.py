""" views of the account app """
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.models import User
from catalog.models import Favorite, Product
from .forms import LoginForm, RegisterForm
# pylint: disable=no-member

# Create your views here.
def log_out(request):
    """method to log out the user"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Vous avez été déconnecté.')
        return redirect('index')
    else:
        messages.error(request, 'Vous devez être connecté.')
        return redirect('index')

def account(request):
    """method to log in the user"""
    template = loader.get_template('account/account.html')
    if request.method == 'POST':
        # A form bound to the POST data
        form_1 = LoginForm(request.POST)
        form_2 = RegisterForm(request.POST)
        # All validation rules pass
        try:
            if form_1.is_valid():
                # Process the data in form.cleaned_data
                user = form_1.cleaned_data['user']
                mdp = form_1.cleaned_data['mdp']
                user = authenticate(username=user, password=mdp)
                login(request, user)
                messages.success(request, 'Vous avez été connecté.')
                request.session.set_expiry(900)
                return redirect('index')
        except:
            messages.error(request, 'Mauvais login/mot de passe.')
            return redirect('account:index')

        if form_2.is_valid():
            mail = form_2.cleaned_data['email']
            username = form_2.cleaned_data['user_name']
            raw_password = form_2.cleaned_data['password']
            try:
                user = User.objects.create_user(username, mail, raw_password)
                messages.success(request, 'Votre compte a été crée.')
                return redirect('index')
            except:
                messages.error(request, 'Votre compte n‘a pas été crée.')
                return redirect('account:index')
    else:
        form_1 = LoginForm()
        form_2 = RegisterForm()

    forms = {
        'form_1': form_1,
        'form_2': form_2,
    }
    return HttpResponse(template.render(forms, request=request))

def favorites(request):
    """method to add a product to favorite products"""
    template = loader.get_template('account/favorites.html')
    if request.user.is_authenticated:
        current_user = request.user
        favorites = Favorite.objects.filter(user_id=current_user.id).order_by('id')
        list_of_favorites = []
        for fav in favorites:
            list_of_favorites.append(Product.objects.filter(id=fav.product_id))
        the_favorites = {
            'list_of_favorites' : list_of_favorites
        }
        return HttpResponse(template.render(the_favorites, request=request))
    else:
        messages.error(request, 'Vous devez être connecté pour voir cette page.')
        return redirect('index')

def profile(request):
    """method to show the user's profile"""
    template = loader.get_template('account/profile.html')
    if request.user.is_authenticated:
        return HttpResponse(template.render(request=request))
    else:
        messages.error(request, 'Vous devez être connecté pour voir cette page.')
        return redirect('index')
