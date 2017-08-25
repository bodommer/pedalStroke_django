from django.conf.urls import url

from . import views

app_name = 'plan'
urlpatterns = [
    url(r'^$', views.IndexView.index, name='index'),
    url(r'^login/$', views.UserView.login, name='login'),
    url(r'^sign-up/$', views.UserView.sign_up, name='sign_up'),
    #url(r'^(?P<user_id>[0-9]+)/$', views.UserView.as_view(), name='user'),
    url(r'^(?P<user_id>[0-9]+)/$', views.UserView.home, name='user'),
    url(r'^(?P<user_id>[0-9]+)/new-season/$', views.SeasonView.new_season, name='new season'),
    url(r'^(?P<user_id>[0-9]+)/season/(?P<season_id>[0-9]+)/$', views.SeasonView.season, name='season'),
    url(r'^(?P<user_id>[0-9]+)/season/(?P<season_id>[0-9]+)/new-race/$', views.RaceView.new_race, name='new race'),
    url(r'^(?P<user_id>[0-9]+)/season/(?P<season_id>[0-9]+)/new-plan/$', views.PlanView.new_plan, name='new plan'),
    url(r'^(?P<user_id>[0-9]+)/plan/(?P<plan_id>[0-9]+)/$', views.PlanView.plan, name='plan'),
    url(r'^about/$', views.IndexView.about, name='about'),
                    
]
