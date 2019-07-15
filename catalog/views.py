"""views.py"""
# Create your views here.
from os import listdir
from os.path import isfile, join
from .database import insert, results
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.defaulttags import register
from .models import *
import json
from django.shortcuts import render, redirect
from django.template.defaulttags import register

@register.filter
def get_range(value):
    return range(1, value)

def catalog(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)

def notices(request):
    template = loader.get_template('catalog/notices.html')
    files = sorted([f for f in listdir('staticfiles/catalog/img') if \
    isfile(join('staticfiles/catalog/img', f))])
    content_picture = [
    "Emoticone triste par <a href='https://www.flaticon.com/free-icon/crying_136366#term=cry&page=1&position=13' target='_blank'>Flaticon</a>", 
    "Colette par <a href='http://personnages-disney.com/Page%20Colette.html' target='_blank'>personnages-disney</a>",
    "Logo de carotte par <a href='https://www.flaticon.com/free-icon/ \
    carrot_1041355#term=carrot&page=1&position=22' target='_blank'>Flaticon</a>",
    "Colette par <a href='https://company-82435.frontify.com/d/6Yy9WFJdtp8j/pur-beurre-style-guide#/introduction/Notre-identité' target='_blank'> Pur Beurre - \
    Charte Graphique </a>",
    "Logo de Pur Beurre par <a href='https://company-82435.frontify.com/d/6Yy9WFJdtp8j/pur-beurre-style-guide#/introduction/Notre-identité' target='_blank'>Pur Beurre - \
    Charte Graphique </a>", 
    "Logo de déconnexion par <a href='https://www.flaticon.com/free-icon/logout_1828490#term=logout&page=1&position=28' target='_blank'>Flaticon</a>",
    "Favicon logo Pur Beurre par <a href='https://www.favicon-generator.org/'>favicon-generator</a>", 
    "Fond d‘écran de la bannière par <a href='https://unsplash.com/photos/eqsEZNCm4-c' target='_blank'> Olenka Kotyk</a>", 
    "Rémy par <a href='https://company-82435.frontify.com/d/6Yy9WFJdtp8j/pur-beurre-style-guide#/introduction/Notre-identité' target='_blank'>\
    Pur Beurre - Charte Graphique </a>",
    "Logo d‘utilisateur par <a href='https://www.flaticon.com/free-icon/ \
    carrot_1041355#term=carrot&page=1&position=22' target='_blank'>Flaticon</a>"
    ]
    d = {x:y for x, y in zip(files, content_picture)}
    context = {
        'd' : d
    }
    return HttpResponse(template.render(context, request=request))

def index(request):
    template = loader.get_template('catalog/index.html')
    insert()
    return HttpResponse(template.render(request=request))

def autocomplete(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        products = Product.objects.filter(name__icontains=query).order_by('id')[:10]
        results = []
        global data
        for p in products:
            product_dict = {}
            product_dict = p.name
            results.append(product_dict)
        data = json.dumps(results)
    else:
	    data = 'fail'
    return HttpResponse(data, 'application/json')

def substitute(request):
    template = loader.get_template('catalog/substitute.html')
    query = request.GET.get('query')
    infos = Product.objects.filter(name=query)
    categories = Category.objects.all()
    global info
    for info in infos:
        pass
    if info is not None:
        try:
            subs = Product.objects.filter(category_id=info.category_id, nutriscore="A").order_by('id')
            if not subs:
                subs = Product.objects.filter(category_id=info.category_id, nutriscore="B").order_by('id')
            if not subs:
                subs = Product.objects.filter(category_id=info.category_id, nutriscore="C").order_by('id')
            for sub in subs:
                pass
            paginator = Paginator(subs, 12)
            num_pages = paginator.num_pages + 1
            page = request.GET.get('page')
            albums = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            albums = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            albums = paginator.page(paginator.num_pages)

        
    substitutes = {
        'query' : query,
        'infos' : infos,
        'info' : info,
        'categories' : categories,
        'subs' : subs,
        'albums': albums,
        'num_pages': num_pages,
        'paginate': True
    }
    return HttpResponse(template.render(substitutes, request=request))

def favorite(request, id):
    messages.success(request, 'Le produit a été ajouté à vos favoris.')
    current_user = request.user
    Favorite.objects.get_or_create(user_id=current_user.id, product_id=id)
    return redirect('index')

def search(request):
    template = loader.get_template('catalog/search.html')
    if request.GET.get('query') is not None:
        global query
        query = request.GET.get('query')
    infos = Product.objects.filter(name__contains=query).order_by('id')
    message = "{}".format(query)
    categories = Category.objects.all()
    global info
    for info in infos:
        pass
    paginator = Paginator(infos, 12)
    num_pages = paginator.num_pages + 1
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)
    message = {
        'message' : message,
        'categories' : categories,
        'infos' : infos,
        'albums': albums,
        'num_pages': num_pages,
        'paginate': True
    }
    return HttpResponse(template.render(message, request=request))

def product(request, product_id):
    template = loader.get_template('catalog/product.html')
    # make sure we have an integer.
    id = int(product_id)
    results(product_id)
    message = results(product_id)
    return HttpResponse(template.render(message, request=request))

