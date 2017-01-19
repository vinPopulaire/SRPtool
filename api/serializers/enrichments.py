from rest_framework import serializers
from api.models import Enrichment


class EnrichmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrichment
        fields = (['enrichment_id','enrichment_class','longName','dbpediaURL','wikipediaURL','description','thumbnail'])
