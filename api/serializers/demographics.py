
from rest_framework import serializers
from api.models import Gender, Age, Education, Occupation, Country


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = (['gender'])

class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        fields = (['age'])

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = (['education'])

class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = (['occupation'])

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (['country'])
