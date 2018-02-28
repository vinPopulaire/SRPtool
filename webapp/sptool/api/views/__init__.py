from .demographics import GenderViewSet
from .demographics import AgeViewSet
from .demographics import OccupationViewSet
from .demographics import EducationViewSet
from .demographics import CountryViewSet
from .demographics import demographics
from .users import UserViewSet
from .videos import VideoViewSet, search_videos
from .actions import ActionViewSet
from .terms import TermViewSet
from .enrichments import EnrichmentViewSet

from .user_actions import user_actions, user_watch
from .recommendations import recommend_videos, recommend_videos_to_target
from .recommendations import recommend_enrichments, recommend_enrichments_to_target
from .recommendations import recommend_friends
from .update_profile import update_profile
from .users import target
from .users import show_friends, add_friend, remove_friend

from .manage_content import import_videos, delete_videos
from .manage_content import import_enrichments, delete_enrichments, delete_enrichments_on_videos