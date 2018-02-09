from django.conf.urls import url, include
from django.contrib.auth.views import logout

from . import views
from pedalStroke import settings

app_name = 'trainings'
urlpatterns = [
    url(r'^$', views.TrainingsView.index, name='overview'),
]