# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import ALBUMS

def listing(request):
    albums = ["<li>{}</li>".format(album['name']) for album in ALBUMS]
    message = """<ul>{}</ul>""".format("\n".join(albums))
    return HttpResponse(message)

def index(request):
    template = loader.get_template('catalog/index.html')
    return HttpResponse(template.render(request=request))

def catalog(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)

def listing(request):
    albums = ["<li>{}</li>".format(album['name']) for album in ALBUMS]
    message = """<ul>{}</ul>""".format("\n".join(albums))
    return HttpResponse(message)