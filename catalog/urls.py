from django.conf.urls import url
from django.urls import path

from . import views # import views so we can use them in urls.

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog, name='index'),
    path('search/', views.search, name='search'),
    path('notices/', views.notices, name='notices'),
]