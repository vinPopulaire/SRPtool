from ..models import Video
from ..serializers import VideoSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework_api_key.permissions import HasAPIAccess

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


class VideoViewSet(viewsets.ModelViewSet):

    permission_classes = (HasAPIAccess,)

    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    lookup_field = "euscreen"


@api_view(['POST'])
@permission_classes((HasAPIAccess, ))
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
            "title": video.title,
            "topic": video.topic,
            "summary": video.summary
        })

    response = Response({"videos": result})

    return response