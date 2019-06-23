from django.conf.urls import url
from django.urls import path

from . import views # import views so we can use them in urls.

app_name = 'account'

urlpatterns = [
    path('', views.account, name='index'),
    path('profile', views.profile, name='profile'),
    path('favorites', views.favorites, name='favorites'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^log_out/$', views.log_out, name='logout')
]