from ..models import Action
from ..serializers import ActionSerializer
from rest_framework import viewsets


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
