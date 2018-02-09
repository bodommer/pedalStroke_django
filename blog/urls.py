from django.conf.urls import url, include

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^all/$', views.BlogGeneralView.listAll, name='list all'),
]