from django.conf.urls import url
from gui import views

urlpatterns = [

    url(r'^$', views.home, name="home"),
    url(r'^terms$', views.terms, name="terms"),
    url(r'^about$', views.about, name="about"),
    url(r'^signup$', views.signup, name="signup")

]