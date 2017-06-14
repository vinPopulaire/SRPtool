from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.algorithms import video_recommendation, find_representatives
from api.models import User, UserContentScore
from api.models import Term


@api_view(['POST'])
def recommend_videos(request, username, *args, **kwargs):

    if "num" in request.data:
        num_req_videos = int(request.data["num"])
    else:
        num_req_videos = 10

    user = User.objects.get(username=username)
    user_id = user.id
    user_content_score = UserContentScore.objects.filter(user_id=user_id).order_by('term_id')

    num_terms = Term.objects.count()

    # Force evaluate queryset for fast .score
    len(user_content_score)
    user_vector = [None] * num_terms

    for ii in range(num_terms):
        user_vector[ii] = user_content_score[ii].score

    videos_list = video_recommendation(user_vector, num_req_videos)

    return Response({"videos": videos_list})


@api_view(['POST'])
def recommend_videos_to_target(request, *args, **kwargs):

    representatives = find_representatives(request)

    # TODO return recommended videos to representatives

    for representative in representatives:
        print(representative)

    message = "recommended videos"
    response = Response({"message": message})

    return response
