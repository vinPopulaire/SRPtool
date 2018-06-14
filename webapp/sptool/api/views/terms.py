from ..models import Term
from ..serializers import TermSerializer
from rest_framework import viewsets

from rest_framework_api_key.permissions import HasAPIAccess


class TermViewSet(viewsets.ModelViewSet):

    permission_classes = (HasAPIAccess,)

    queryset = Term.objects.all()
    serializer_class = TermSerializer
