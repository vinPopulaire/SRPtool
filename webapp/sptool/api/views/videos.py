from ..models import Video
from ..serializers import VideoSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    lookup_field = "euscreen"


@api_view(['POST'])
def search_videos(request, *args, **kwargs):

    if "query" in request.data:
        keywords = request.data["query"]
    else:
        return Response({"message": "no search query provided"})

    query = SearchQuery(keywords)

    topic_vector = SearchVector('topic', weight='A')
    title_vector = SearchVector('title', weight='B')
    summary_vector = SearchVector('summary', weight='C')
    vectors = topic_vector + title_vector + summary_vector

    qs = Video.objects.all()

    qs = qs.annotate(search=vectors).filter(search=query)
    qs = qs.annotate(rank=SearchRank(vectors, query)).order_by('-rank')

    result = []
    for video in qs:
        result.append({
            "euscreen": video.euscreen,
            "video": video.title,
            "topic": video.topic,
            "summary": video.summary
        })

    response = Response({"videos": result})

    return response