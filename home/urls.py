from django.conf.urls import url, include
from django.contrib import admin

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^about/', views.HomeViews.aboutPage, name='about'),
    url(r'^home/', views.HomeViews.indexPage, name='home'),
    url(r'^sign-up/', views.HomeViews.sign_up, name='sign_up'),
    url(r'^login/', views.HomeViews.login, name='login'),
    url(r'^access-denied/', views.HomeViews.request_denied, name='request denied'),
    url(r'^logout/', views.logout, name='logout'),
]