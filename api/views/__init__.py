from .demographics import GenderViewSet
from .demographics import AgeViewSet
from .demographics import OccupationViewSet
from .demographics import EducationViewSet
from .demographics import CountryViewSet
from .users import UserViewSet
from .videos import VideoViewSet
from .actions import ActionViewSet
from .terms import TermViewSet
from .enrichments import EnrichmentViewSet

from .user_actions import user_actions, user_watch
from .recommendations import recommend_videos, recommend_videos_to_target
from .recommendations import recommend_enrichments, recommend_enrichments_to_target
from .update_profile import update_profile
from .users import target
