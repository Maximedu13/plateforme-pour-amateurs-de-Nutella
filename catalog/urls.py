from django.conf.urls import url
from django.urls import path

from . import views # import views so we can use them in urls.

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog, name='index'),
    path('search', views.search, name='search'),
    path('notices/', views.notices, name='notices'),
    path('substitute', views.substitute, name='search-a-substitute'),
    path('catalog/<str:product_id>', views.product, name='detail'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    #path('ajax/', views.ajax, name='ajax'),
    #path("catalog/<str:product_id>", views.product, name="id"),
]