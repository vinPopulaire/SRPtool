from rest_framework import serializers
from ..models import Term


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = (["term"])
