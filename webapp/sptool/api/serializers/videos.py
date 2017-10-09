from rest_framework import serializers
from ..models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (['euscreen','genre','topic','title','geographical_coverage','thesaurus_terms','summary'])
