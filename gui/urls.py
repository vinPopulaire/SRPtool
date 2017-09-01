from django.conf.urls import url
from gui import views

urlpatterns = [

    url(r'^$', views.home),
    url(r'^terms$', views.terms),
    url(r'^about$', views.about),
    url(r'^signup$', views.signup)

]