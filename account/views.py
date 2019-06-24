""" views of the account app """
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from catalog.models import Favorite, Product
from .forms import LoginForm, RegisterForm

# Create your views here.
def log_out(request):
    """method to log out the user"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté.')
    return redirect('index')


def account(request):
    """method to log in the user"""
    template = loader.get_template('account/account.html')
    if request.method == 'POST':
        # A form bound to the POST data
        form_1 = LoginForm(request.POST)
        form_2 = RegisterForm(request.POST)
        username = request.POST.get('user')
        pword = request.POST.get('mdp')
        mail = request.POST.get('email')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        print(mail, user_name, password)
        # All validation rules pass
        if form_1.is_valid():
            # Process the data in form.cleaned_data
            user = form_1.cleaned_data['user']
            mdp = form_1.cleaned_data['mdp']
            user = authenticate(username=user, password=mdp)
            login(request, user)
            messages.success(request, 'Vous avez été connecté.')
            request.session.set_expiry(900)
            return redirect('index')
        if form_2.is_valid():
            print("valid")
            email = form_2.cleaned_data['email']
            username = form_2.cleaned_data['user_name']
            raw_password = form_2.cleaned_data['password']
            try:
                user = User.objects.create_user(username, mail, raw_password)
                return redirect('index')
            except:
                print("lol")
    else:
        form_1 = LoginForm() # An unbound form
        form_2 = RegisterForm()


    return render(request, 'account/account.html', {
        'form_1': form_1,
        'form_2': form_2,
    })

def favorites(request):
    """method to add a product to favorite products"""
    template = loader.get_template('account/favorites.html')
    current_user = request.user
    favorites = Favorite.objects.filter(user_id=current_user.id).order_by('id')
    list_of_favorites = []
    for fav in favorites:
        list_of_favorites.append(Product.objects.filter(id=fav.product_id))
    the_favorites = {
        'list_of_favorites' : list_of_favorites
    }
    return HttpResponse(template.render(the_favorites, request=request))

def profile(request):
    """method to show the user's profile"""
    template = loader.get_template('account/profile.html')
    return HttpResponse(template.render(request=request))
