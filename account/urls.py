from django.conf.urls import url
from django.urls import path

from . import views # import views so we can use them in urls.

app_name = 'account'

urlpatterns = [
    path('', views.account, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
]