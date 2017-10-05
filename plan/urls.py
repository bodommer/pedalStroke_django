from django.conf.urls import url, include

from . import views

app_name = 'plan'
urlpatterns = [
    url(r'^$', views.IndexView.index, name='index'),
    url(r'^login/$', views.UserView.login, name='login'),
    url(r'^sign-up/$', views.UserView.sign_up, name='sign_up'),
    #url(r'^(?P<user_id>[0-9]+)/$', views.UserView.as_view(), name='user'),
    url(r'^(?P<user_id>[0-9]+)/$', views.UserView.home, name='user'),
    url(r'^(?P<user_id>[0-9]+)/profile/$', views.UserView.profile, name='profile'),
    url(r'^(?P<user_id>[0-9]+)/profile/edit/$', views.UserView.profileEdit, name='profile edit'),
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
    url(r'^about/$', views.IndexView.about, name='about'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    views.UserView.activate, name='activate'),
    url(r'^logout/', views.logout, name='logout'),
]
