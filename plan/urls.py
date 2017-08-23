from django.conf.urls import url

from . import views

app_name = 'plan'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^sign-up/$', views.sign_up, name='sign_up'),
    url(r'^(?P<pk>[0-9]+)/$', views.UserView.as_view(), name='user'),
    url(r'^new-season/$', views.new_season, name='new season'),
    url(r'^new-race/$', views.new_race, name='new race'),
    url(r'^(?P<user_id>[0-9]+)/(?P<season_id>[0-9]+)/$', views.season, name='season'),
    url(r'^new-plan/$', views.new_plan, name='new-plan'),
    url(r'^(?P<user_id>[0-9]+)/plans/(?P<plan_id>[0-9]+)/$', views.plan, name='plan'),
    url(r'^about/$', views.about, name='about'),
                    
]
