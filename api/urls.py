from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from api import views

from api.views import GenderViewSet
from api.views import AgeViewSet
from api.views import EducationViewSet
from api.views import OccupationViewSet
from api.views import CountryViewSet


router = routers.DefaultRouter()
router.register(r'gender', GenderViewSet)
router.register(r'age', AgeViewSet)
router.register(r'education', EducationViewSet)
router.register(r'occupation', OccupationViewSet)
router.register(r'country', CountryViewSet)

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
        name='video_detail'),

    url(r'^api/', include(router.urls)),

]
