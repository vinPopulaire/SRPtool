from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^api/$',
        views.UserList.as_view(),
        name='user_list'),
    url(r'^api/(?P<username>[a-z0-9]+)/$',
        views.UserDetail.as_view(),
        name='user_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
