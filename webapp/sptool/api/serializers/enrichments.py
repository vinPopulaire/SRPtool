from rest_framework import serializers
from ..models import Enrichment


class EnrichmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrichment
        fields = (['enrichment_id','name','thumbnail','title','overlay_title','overlay_text_description', 'dbpediaURL', 'wikipediaURL', 'enrichment_class'])
