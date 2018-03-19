from rest_framework import serializers
from ..models import Enrichment


class EnrichmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrichment
        fields = (['enrichment_id','name','title','overlay_title','overlay_text_description'])
