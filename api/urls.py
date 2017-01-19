from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from api import views

from api.views import GenderViewSet
from api.views import AgeViewSet
from api.views import EducationViewSet
from api.views import OccupationViewSet
from api.views import CountryViewSet
from api.views import VideoViewSet
from api.views import UserViewSet
from api.views import ActionViewSet
from api.views import TermViewSet
from api.views import EnrichmentViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'video', VideoViewSet)
router.register(r'gender', GenderViewSet)
router.register(r'age', AgeViewSet)
router.register(r'education', EducationViewSet)
router.register(r'occupation', OccupationViewSet)
router.register(r'country', CountryViewSet)
router.register(r'action', ActionViewSet)
router.register(r'term', TermViewSet)
router.register(r'enrichment', EnrichmentViewSet)

urlpatterns = [

    url(r'^api/', include(router.urls)),

]
