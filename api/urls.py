from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [

    url(r'^api/gender/$',
        views.GenderList.as_view(),
        name='gender_list'),
    url(r'^api/gender/(?P<pk>[0-9]+)/$',
        views.GenderDetail.as_view(),
        name='gender_detail'),

    url(r'^api/age/$',
        views.AgeList.as_view(),
        name='age_list'),
    url(r'^api/age/(?P<pk>[0-9]+)/$',
        views.AgeDetail.as_view(),
        name='age_detail'),

    url(r'^api/education/$',
        views.EducationList.as_view(),
        name='education_list'),
    url(r'^api/education/(?P<pk>[0-9]+)/$',
        views.EducationDetail.as_view(),
        name='education_detail'),

    url(r'^api/occupation/$',
        views.OccupationList.as_view(),
        name='occupation_list'),
    url(r'^api/occupation/(?P<pk>[0-9]+)/$',
        views.OccupationDetail.as_view(),
        name='occupation_detail'),

    url(r'^api/country/$',
        views.CountryList.as_view(),
        name='country_list'),
    url(r'^api/country/(?P<pk>[0-9]+)/$',
        views.CountryDetail.as_view(),
        name='country_detail'),

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
