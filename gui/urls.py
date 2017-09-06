from django.conf.urls import url
from gui import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    url(r'^$', views.home, name="home"),
    url(r'^terms/$', views.terms, name="terms"),
    url(r'^about/$', views.about, name="about"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^login/$', auth_views.login, {'template_name': 'gui/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^delete_user/$', views.delete, name="delete")

]
