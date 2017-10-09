from rest_framework import serializers
from ..models import Gender, Age, Education, Occupation, Country


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = (['id', 'gender'])


class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        fields = (['id', 'age'])


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = (['id', 'education'])


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = (['id', 'occupation'])


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (['id', 'country'])
