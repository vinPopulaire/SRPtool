from ..models import Gender, Age, Occupation, Education, Country
from ..serializers import GenderSerializer, AgeSerializer, OccupationSerializer, EducationSerializer, CountrySerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response


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


@api_view(['GET'])
def demographics(request, *args, **kwargs):
    genders = Gender.objects.all()
    genders_serializer = GenderSerializer(genders, many=True)

    ages = Age.objects.all()
    ages_serializer = AgeSerializer(ages, many=True)

    occupations = Occupation.objects.all()
    occupations_serializer = OccupationSerializer(occupations, many=True)

    educations = Education.objects.all()
    educations_serializer = EducationSerializer(educations, many=True)

    countries = Country.objects.all()
    countries_serializer = CountrySerializer(countries, many=True)

    return Response({
        'genders': genders_serializer.data,
        'ages': ages_serializer.data,
        'occupations': occupations_serializer.data,
        'educations': educations_serializer.data,
        'countries': countries_serializer.data,
    })