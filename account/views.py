from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm

# Create your views here.
def account(request):
    template = loader.get_template('account/account.html')
    if request.method == 'POST': # Si le formulaire a été envoyé...
        form_1 = LoginForm(request.POST) # A form bound to the POST data
        form_2 = RegisterForm(request.POST)
        if form_1.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            user = form_1.cleaned_data['user']
            mdp = form_1.cleaned_data['mdp']
            return redirect("/account")
    else:
        form_1 = LoginForm() # An unbound form
        form_2 = RegisterForm()

    return render(request, 'account/account.html', {
        'form_1': form_1,
        'form_2': form_2
    })
    return HttpResponse(template.render(request=request))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})