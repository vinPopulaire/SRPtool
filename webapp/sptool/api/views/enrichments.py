from ..models import Enrichment
from ..serializers import EnrichmentSerializer
from rest_framework import viewsets


class EnrichmentViewSet(viewsets.ModelViewSet):
    queryset = Enrichment.objects.all()
    serializer_class = EnrichmentSerializer

    lookup_field = "enrichment_id"
