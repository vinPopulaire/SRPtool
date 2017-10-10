from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    url(r'^$', views.home, name="home"),
    url(r'^terms/$', views.terms, name="terms"),
    url(r'^about/$', views.about, name="about"),

    url(r'^signup/$', views.signup, name="signup"),
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^login/$', auth_views.login, {'template_name': 'gui/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^delete_user/$', views.delete, name="delete"),

    url(r'^videos/$', views.videos, name="videos"),
    url(r'^videos/(?P<euscreen>[0-9 a-zA-Z_]+)/$', views.play_video, name="play_video"),

    url(r'^business/$', views.business, name="business"),

]