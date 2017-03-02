from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.algorithms import video_recommendation


@api_view(['POST'])
def recommend_videos(request, username, *args, **kwargs):

    videos_list = video_recommendation(request, username)

    return Response({"videos": videos_list})
