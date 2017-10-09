from ..models import Video
from ..serializers import VideoSerializer
from rest_framework import viewsets


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    lookup_field = "euscreen"
