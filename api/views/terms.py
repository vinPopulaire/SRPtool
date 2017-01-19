from api.models import Term
from api.serializers import TermSerializer
from rest_framework import viewsets


class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
