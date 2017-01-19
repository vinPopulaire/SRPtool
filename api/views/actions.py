from api.models import Action
from api.serializers import ActionSerializer
from rest_framework import viewsets


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
