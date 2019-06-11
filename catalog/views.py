"""views.py"""
# Create your views here.
from os import listdir
from os.path import isfile, join
from .database import insert
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from django.template.defaulttags import register
from .models import *

@register.filter
def get_range(value):
    return range(value)

def catalog(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)

def notices(request):
    template = loader.get_template('catalog/notices.html')
    files = [f for f in listdir('catalog/static/catalog/img') if \
    isfile(join('catalog/static/catalog/img', f))]
    files.remove('.DS_Store')
    content_picture = ["Fond d‘écran de la bannière par \
    <a href='https://unsplash.com/photos/eqsEZNCm4-c' target='_blank'> Olenka Kotyk</a>", \
    "Colette par <a href='https://company-82435.frontify.com/d/6Yy9WFJdtp8j/pur-beurre-style-guide#/introduction/Notre-identité' target='_blank'> Pur Beurre - \
    Charte Graphique </a>", "Logo d‘utilisateur par <a href='https://www.flaticon.com/free-icon/ \
    carrot_1041355#term=carrot&page=1&position=22' target='_blank'>Flaticon</a>", \
    "Logo de carotte par <a href='https://www.flaticon.com/free-icon/ \
    carrot_1041355#term=carrot&page=1&position=22' target='_blank'>Flaticon</a>", \
    "Logo de Pur Beurre par <a href='https://company-82435.frontify.com/d/6Yy9WFJdtp8j/pur-beurre-style-guide#/introduction/Notre-identité' target='_blank'>Pur Beurre - \
    Charte Graphique </a>", "Rémy par <a href='https://company-82435.frontify.com/d/6Yy9WFJdtp8j/pur-beurre-style-guide#/introduction/Notre-identité' target='_blank'>\
    Pur Beurre - Charte Graphique </a>", "Favicon logo Pur Beurre par \
    <a href='https://www.favicon-generator.org/'>favicon-generator</a>"]
    d = {x:y for x, y in zip(files, content_picture)}
    context = {
        'd' : d
    }
    return HttpResponse(template.render(context, request=request))

def index(request):
    template = loader.get_template('catalog/index.html')
    return HttpResponse(template.render(request=request))

def search(request):
    template = loader.get_template('catalog/search.html')
    query = request.GET.get('query')
    obj = str(request.GET)
    message = "propriété GET : {} et requête : {}".format(obj, query)
    insert()
    Category.objects.filter()[:12]
    categories = Category.objects.all()
    formatted_categories = ["{}".format(album.name) for album in categories]
    categories = """<ul>{}</ul>""".format("\n".join(formatted_categories))
    message = {
        'message' : message,
        'categories' : categories
    }
    return HttpResponse(template.render(message, request=request))
