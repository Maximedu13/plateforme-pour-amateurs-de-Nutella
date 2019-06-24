""" urls form the account app """
from django.urls import path
from . import views # import views so we can use them in urls.

app_name = 'account'

urlpatterns = [
    path('', views.account, name='index'),
    path('profile', views.profile, name='profile'),
    path('favorites', views.favorites, name='favorites'),
    path('log_out', views.log_out, name='logout')
]
