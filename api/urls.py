from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^api/user/$',
        views.UserList.as_view(),
        name='user_list'),
    url(r'^api/user/(?P<username>[A-Za-z0-9]+)/$',
        views.UserDetail.as_view(),
        name='user_detail'),
    url(r'^api/video/$',
        views.VideoList.as_view(),
        name='video_list'),
    url(r'^api/video/(?P<euscreen>[A-Za-z0-9]+)/$',
        views.VideoDetail.as_view(),
        name='video_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
