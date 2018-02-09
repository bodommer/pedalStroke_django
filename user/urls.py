from django.conf.urls import url, include

from . import views

app_name = 'user'
urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/profile/$', views.ProfileView.profile, name='profile'),
    url(r'^(?P<user_id>[0-9]+)/profile/edit/$', views.ProfileView.profileEdit, name='profile edit'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.ProfileView.activate, name='activate'),
]