from django.conf.urls import url, include
from django.contrib.auth.views import logout

from . import views
from pedalStroke import settings

app_name = 'plan'
urlpatterns = [
    #url(r'^$', views.IndexView.index, name='index'),
    #url(r'^(?P<user_id>[0-9]+)/$', views.UserView.as_view(), name='user'),
    url(r'^(?P<user_id>[0-9]+)/$', views.UserView.home, name='user'),
    url(r'^(?P<user_id>[0-9]+)/season/(?P<season_id>[0-9]+)/$', views.SeasonView.season, name='season'),
    url(r'^(?P<user_id>[0-9]+)/new-season/$', views.SeasonView.new_season, name='new season'),
    url(r'^(?P<user_id>[0-9]+)/season/(?P<season_id>[0-9]+)/delete-season/$', views.SeasonView.seasonDelete, name='delete season'),
    url(r'^(?P<user_id>[0-9]+)/plan/(?P<plan_id>[0-9]+)/$', views.PlanView.plan, name='plan'),
    url(r'^(?P<user_id>[0-9]+)/season/(?P<season_id>[0-9]+)/new-plan/$', views.PlanView.new_plan, name='new plan'),
    url(r'^(?P<user_id>[0-9]+)/season/(?P<season_id>[0-9]+)/plan-delete/$', views.PlanView.planDelete, name='delete plans'),
    url(r'^(?P<user_id>[0-9]+)/season/(?P<season_id>[0-9]+)/race/(?P<race_id>[0-9]+)/$', views.RaceView.race, name='race'),
    url(r'^(?P<user_id>[0-9]+)/season/(?P<season_id>[0-9]+)/new-race/$', views.RaceView.new_race, name='new race'),
    url(r'^(?P<user_id>[0-9]+)/season/(?P<season_id>[0-9]+)/race/(?P<race_id>[0-9]+)/edit/$', views.RaceView.raceEdit, name='race edit'),
    url(r'^(?P<user_id>[0-9]+)/season/(?P<season_id>[0-9]+)/race-delete/$', views.RaceView.raceDelete, name='delete races'),
]
