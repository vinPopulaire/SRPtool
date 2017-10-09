from api.models import Gender, Age, Occupation, Education, Country
from api.serializers import GenderSerializer, AgeSerializer, OccupationSerializer, EducationSerializer, CountrySerializer
from rest_framework import generics
from rest_framework import viewsets


class GenderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class AgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Age.objects.all()
    serializer_class = AgeSerializer


class OccupationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer


class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
