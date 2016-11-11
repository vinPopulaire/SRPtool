from api.models import Gender, Age, Occupation, Education, Country
from api.serializers import GenderSerializer, AgeSerializer, OccupationSerializer, EducationSerializer, CountrySerializer
from rest_framework import generics


class GenderList(generics.ListAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer

class GenderDetail(generics.RetrieveAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class AgeList(generics.ListAPIView):
    queryset = Age.objects.all()
    serializer_class = AgeSerializer

class AgeDetail(generics.RetrieveAPIView):
    queryset = Age.objects.all()
    serializer_class = AgeSerializer


class OccupationList(generics.ListAPIView):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer

class OccupationDetail(generics.RetrieveAPIView):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer


class EducationList(generics.ListAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

class EducationDetail(generics.RetrieveAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class CountryList(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryDetail(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
