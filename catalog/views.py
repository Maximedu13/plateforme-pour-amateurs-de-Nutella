"""views.py"""
# Create your views here.
from os import listdir
from os.path import isfile, join
from .database import insert
from django.http import HttpResponse
from django.template import loader
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
    files = [f for f in listdir('staticfiles/catalog/img') if \
    isfile(join('staticfiles/catalog/img', f))]
    print(files)
    content_picture = [
    "Logo de déconnexion par <a href='https://www.flaticon.com/free-icon/logout_1828490#term=logout&page=1&position=28' target='_blank'>Flaticon</a>",
    "Rémy par <a href='https://company-82435.frontify.com/d/6Yy9WFJdtp8j/pur-beurre-style-guide#/introduction/Notre-identité' target='_blank'>\
    Pur Beurre - Charte Graphique </a>", 
    "Colette par <a href='http://personnages-disney.com/Page%20Colette.html' target='_blank'>personnages-disney</a>",
    "Logo d‘utilisateur par <a href='https://www.flaticon.com/free-icon/ \
    carrot_1041355#term=carrot&page=1&position=22' target='_blank'>Flaticon</a>", 
    "Logo de Pur Beurre par <a href='https://company-82435.frontify.com/d/6Yy9WFJdtp8j/pur-beurre-style-guide#/introduction/Notre-identité' target='_blank'>Pur Beurre - \
    Charte Graphique </a>", 
    "Emoticone triste par <a href='https://www.flaticon.com/free-icon/crying_136366#term=cry&page=1&position=13' target='_blank'>Flaticon</a>", 
    "Favicon logo Pur Beurre par <a href='https://www.favicon-generator.org/'>favicon-generator</a>", 
    "Logo de carotte par <a href='https://www.flaticon.com/free-icon/ \
    carrot_1041355#term=carrot&page=1&position=22' target='_blank'>Flaticon</a>",
    "Fond d‘écran de la bannière par <a href='https://unsplash.com/photos/eqsEZNCm4-c' target='_blank'> Olenka Kotyk</a>", 
    "Colette par <a href='https://company-82435.frontify.com/d/6Yy9WFJdtp8j/pur-beurre-style-guide#/introduction/Notre-identité' target='_blank'> Pur Beurre - \
    Charte Graphique </a>"
    ]
    print(len(content_picture))
    d = {x:y for x, y in zip(files, content_picture)}
    context = {
        'd' : d
    }
    return HttpResponse(template.render(context, request=request))

def index(request):
    template = loader.get_template('catalog/index.html')
    return HttpResponse(template.render(request=request))

def autocomplete(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        products = Product.objects.filter(name__icontains=query).order_by('id')[:10]
        results = []
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
    insert()
    infos = Product.objects.filter(name=query)
    categories = Category.objects.all()
    global info
    for info in infos:
        pass
    for category in categories:
        pass

    subs = Product.objects.filter(category_id=info.category_id, nutriscore="A")
    if not subs:
        subs = Product.objects.filter(category_id=info.category_id, nutriscore="B")
    if not subs:
        subs = Product.objects.filter(category_id=info.category_id, nutriscore="C")

    for sub in subs:
        pass

    paginator = Paginator(subs, 12)
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
    substitutes = {
        'query' : query,
        'info' : info,
        'categories' : categories,
        'subs' : subs,
        'albums': albums,
        'num_pages': num_pages,
        'paginate': True
    }
    return HttpResponse(template.render(substitutes, request=request))

def favorite(request, id):
    message = "Produit ajouté aux favoris"
    current_user = request.user
    Favorite.objects.get_or_create(user_id=current_user.id, product_id=id)
    return redirect('index')
    return HttpResponse(message)

def search(request):
    template = loader.get_template('catalog/search.html')
    query = request.GET.get('query')
    obj = str(request.GET)
    #message = "propriété GET : {} et requête : {}".format(obj, query)
    message = "{}".format(query)
    insert()
    categories = Category.objects.all()
    products = Product.objects.filter(name__contains=query).order_by('id')
    # Slice pages
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    print(page)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    print(len(products))
    if not products:
        print("aucun res")
    """for product in products:
        print(product.proteins)"""

    for product in products:
        product_id = product.id
        #print(product.nutriscore)

    formatted_categories = ["{}".format(album.name) for album in categories]
    categories = """<ul>{}</ul>""".format("\n".join(formatted_categories))

    formatted_images = ["<img src='{}' class='img-fluid img-thumbnail'>".format(product.image) for product in products]
    images = """{}""".format("\n".join(formatted_images))

    formatted_names = ["{}".format(product.name) for product in products]
    names = """{}""".format("\n".join(formatted_names)) 

    formatted_nutri = ["{}".format(product.nutriscore) for product in products]
    nutri_score = """{}""".format("\n".join(formatted_nutri)) 

    formatted_id = ["{}".format(product.id) for product in products]
    global ID
    ID = """{}""".format("\n".join(formatted_id)) 

    message = {
        'message' : message,
        'categories' : categories,
        'products' : products,
        'images' : images,
        'names' : names,
        'nutri_score' : nutri_score,
        'ID' : ID
    }
    return HttpResponse(template.render(message, request=request))

def product(request, product_id):
    template = loader.get_template('catalog/product.html')
    id = int(product_id) # make sure we have an integer.
    this_product = Product.objects.get(pk=id)
    this_product.proteins = this_product.proteins.__round__ (2)
    this_product.formatted_proteins = "Protéines : {} g/100g".format(this_product.proteins.__round__(2))
    this_product.formatted_calories = "Calories : {} kCal/100g".format(this_product.calories.__round__(2))
    this_product.salts = this_product.salts.__round__(2)
    this_product.formatted_salts = "Sel : {} g/100g".format(this_product.salts)
    this_product.formatted_lipids = "Lipides : {} g/100g".format(this_product.lipids.__round__(2))
    this_product.sugars = this_product.sugars.__round__ (2)
    this_product.formatted_sugars = "Sucres : {} g/100g".format(this_product.sugars.__round__(2))
    
    salts_percentage = this_product.salts * 100 / 2.3
    salts_percentage = str(salts_percentage) + "%"
    proteins_percentage = this_product.proteins * 100 / 16
    proteins_percentage = str(proteins_percentage) + "%"
    sugars_percentage = this_product.sugars * 100 / 45
    sugars_percentage = str(sugars_percentage) + "%"
    lipids_percentage = this_product.lipids * 100 / 60
    lipids_percentage = str(lipids_percentage) + "%"
    calories_percentage = this_product.calories * 100 / 560
    calories_percentage = str(calories_percentage) + "%"

    low = "Peu"
    medium = "Un peu trop"
    high = "Trop"
    space = " "
    adjective_calories = "calorique"
    adjective_sugars = "sucré"
    adjective_salts = "salé"
    adjective_proteins = "protéiné"
    adjective_lipids = "lipidique"

    if this_product.calories < 560 /3:
        result_nutri_score_cal = low + space + adjective_calories
    elif this_product.calories >= 560 / 3 and this_product.calories <= 560 / 2:
        result_nutri_score_cal = medium + space + adjective_calories
    else:
        result_nutri_score_cal = high + space + adjective_calories

    if this_product.proteins < 16/3:
        result_nutri_score_pro = low + space + adjective_proteins
    elif this_product.proteins >= 16/3 and this_product.proteins <= 16/2:
        result_nutri_score_pro = "Un peu " + adjective_proteins
    else:
        result_nutri_score_pro = "Bonne source de protéines"
    
    if this_product.lipids < 60/3:
        result_nutri_score_lpds = low + space + adjective_lipids
    elif this_product.lipids >= 60/3 and this_product.lipids <= 60/2:
        result_nutri_score_lpds = medium + space + adjective_lipids
    else:
        result_nutri_score_lpds = high + space + adjective_lipids


    if this_product.salts < 2.3/3:
        result_nutri_score_salts = low + space + adjective_salts
    elif this_product.salts >= 2.3/3 and this_product.salts <= 2.3/2 :
        result_nutri_score_salts = medium + space + adjective_salts
    else:
        result_nutri_score_salts = high + space + adjective_salts
    
    if this_product.sugars < 45/3:
        result_nutri_score_sugars = low + space + adjective_sugars
    elif this_product.sugars >= 45/3 and this_product.sugars <= 45/2 :
        result_nutri_score_sugars = medium + space + adjective_sugars
    else:
        result_nutri_score_sugars = high + space + adjective_sugars

    message = {
        'this_product' : this_product,
        'lipids_percentage' : lipids_percentage,
        'calories_percentage' : calories_percentage,
        'salts_percentage' : salts_percentage,
        'result_nutri_score_cal' : result_nutri_score_cal,
        'result_nutri_score_pro' : result_nutri_score_pro,
        'result_nutri_score_salts' : result_nutri_score_salts,
        'result_nutri_score_sugars' : result_nutri_score_sugars,
        'result_nutri_score_lpds' : result_nutri_score_lpds,
        'proteins_percentage' : proteins_percentage,
        'sugars_percentage' : sugars_percentage
    }
    
    return HttpResponse(template.render(message, request=request))

