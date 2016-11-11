from rest_framework import serializers
from api.models import User, Video


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','name', 'surname','email','gender','age','education','occupation','country')

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('euscreen','genre','topic','title','geographical_coverage','thesaurus_terms','summary')
