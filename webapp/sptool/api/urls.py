from django.conf.urls import url, include
from rest_framework import routers
from . import views

from .views import GenderViewSet
from .views import AgeViewSet
from .views import EducationViewSet
from .views import OccupationViewSet
from .views import CountryViewSet
from .views import VideoViewSet
from .views import UserViewSet
from .views import ActionViewSet
from .views import TermViewSet
from .views import EnrichmentViewSet

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

    url(r'^', include(router.urls)),

    url(r'^demographics/', views.demographics),

    url(r'^user/(?P<username>[0-9 a-z.A-Z_]+)/watch$', views.user_watch),
    url(r'^user/(?P<username>[0-9 a-z.A-Z_]+)/actions$', views.user_actions),

    url(r'^user/(?P<username>[0-9 a-z.A-Z_]+)/recommend_videos$', views.recommend_videos),

    url(r'^user/(?P<username>[0-9 a-z.A-Z_]+)/update_profile$', views.update_profile),

    url(r'^user/(?P<username>[0-9 a-z.A-Z_]+)/friends$', views.show_friends),
    url(r'^user/(?P<username>[0-9 a-z.A-Z_]+)/add_friend$', views.add_friend),
    url(r'^user/(?P<username>[0-9 a-z.A-Z_]+)/remove_friend$', views.remove_friend),
    url(r'^user/(?P<username>[0-9 a-z.A-Z_]+)/recommend_friends$', views.recommend_friends),

    url(r'^search_videos$', views.search_videos),

    url(r'^target$', views.target),
    url(r'^videos_to_target$', views.recommend_videos_to_target),

    url(r'^user/(?P<username>[0-9 a-z.A-Z_]+)/recommend_enrichments$', views.recommend_enrichments),
    url(r'^user/(?P<username>[0-9 a-z.A-Z_]+)/enrichments_from_set$', views.recommend_enrichment_from_set),
    url(r'^enrichments_to_target$', views.recommend_enrichments_to_target),
    url(r'^enrichments_to_target_for_IEVCT', views.recommend_enrichments_to_target_for_IEVCT),

    url(r'^import_video$', views.import_video),
    url(r'^delete_videos$', views.delete_videos),

    url(r'^import_enrichments$', views.import_enrichments),
    url(r'^delete_enrichments$', views.delete_enrichments),
    url(r'^delete_enrichments_on_videos$', views.delete_enrichments_on_videos),
    url(r'^delete_enrichments_on_project$', views.delete_enrichments_on_project)
]
