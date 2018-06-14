from ..models import Action
from ..serializers import ActionSerializer
from rest_framework import viewsets

from rest_framework_api_key.permissions import HasAPIAccess


class ActionViewSet(viewsets.ModelViewSet):

    permission_classes = (HasAPIAccess,)

    queryset = Action.objects.all()
    serializer_class = ActionSerializer
