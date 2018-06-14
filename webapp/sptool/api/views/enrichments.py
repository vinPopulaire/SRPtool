from ..models import Enrichment
from ..serializers import EnrichmentSerializer
from rest_framework import viewsets

from rest_framework_api_key.permissions import HasAPIAccess


class EnrichmentViewSet(viewsets.ModelViewSet):

    permission_classes = (HasAPIAccess,)

    queryset = Enrichment.objects.all()
    serializer_class = EnrichmentSerializer

    lookup_field = "enrichment_id"
