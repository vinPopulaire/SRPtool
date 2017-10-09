from rest_framework import serializers
from api.models import Action


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ("action","importance")
