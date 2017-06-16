from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.algorithms import video_recommendation, find_representatives
from api.algorithms import top_enrichments_recommendation, enrichments_recommendation
from api.models import User, UserContentScore
from api.models import Term
from api.models import Video


@api_view(['POST'])
def recommend_videos(request, username, *args, **kwargs):

    if "num" in request.data:
        num_req_videos = int(request.data["num"])
    else:
        num_req_videos = 10

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": "user does not exist"})

    user_id = user.id
    user_content_score = UserContentScore.objects.filter(user_id=user_id).order_by('term_id')

    num_terms = Term.objects.count()

    # Force evaluate queryset for fast .score
    len(user_content_score)
    user_vector = [None] * num_terms

    for ii in range(num_terms):
        user_vector[ii] = float(user_content_score[ii].score)

    videos_list = video_recommendation(user_vector, num_req_videos)

    return Response({"videos": videos_list})


@api_view(['POST'])
def recommend_videos_to_target(request, *args, **kwargs):

    if "num" in request.data:
        num_req_videos = int(request.data["num"])
    else:
        num_req_videos = 10

    representatives = find_representatives(request)

    # create json output of representatives with videos
    videos = {}
    for i in range(0, len(representatives)):

        videos['representative %d' % (i + 1)] = video_recommendation(representatives[i], num_req_videos)

    if representatives:
        response = Response(videos)
    else:
        response = Response({"message": "no information on target group"})

    return response


@api_view(['POST'])
def top_enrichments(request, username, *args, **kwargs):

    if "num" in request.data:
        num_enrichments = int(request.data["num"])
    else:
        num_enrichments = 10

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": "user does not exist"})

    if "euscreen" in request.data:
        euscreen = request.data["euscreen"]
    else:
        return Response({"message": "specific video must be selected"})

    try:
        video = Video.objects.get(euscreen=euscreen)
    except Video.DoesNotExist:
        return Response({"message": "video does not exist"})

    user_content_score = UserContentScore.objects.filter(user_id=user.id).order_by('term_id')

    num_terms = Term.objects.count()

    # Force evaluate queryset for fast .score
    len(user_content_score)
    user_vector = [None] * num_terms

    for ii in range(num_terms):
        user_vector[ii] = float(user_content_score[ii].score)

    enrichments_list = top_enrichments_recommendation(user_vector, video.id, num_enrichments)

    return Response({"enrichments": enrichments_list})


@api_view(['POST'])
def recommend_top_enrichments_to_target(request, *args, **kwargs):

    if "num" in request.data:
        num_enrichments = int(request.data["num"])
    else:
        num_enrichments = 10

    if "euscreen" in request.data:
        euscreen = request.data["euscreen"]
    else:
        return Response({"message": "specific video must be selected"})

    try:
        video = Video.objects.get(euscreen=euscreen)
    except Video.DoesNotExist:
        return Response({"message": "video does not exist"})

    representatives = find_representatives(request)

    # create json output of representatives with videos
    enrichments = {}
    for i in range(0, len(representatives)):
        enrichments['representative %d' % (i + 1)] = top_enrichments_recommendation(representatives[i], video.id, num_enrichments)

    if representatives:
        response = Response(enrichments)
    else:
        response = Response({"message": "no information on target group"})

    return response


@api_view(['POST'])
def recommend_enrichments(request, username, *args, **kwargs):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": "user does not exist"})

    if "euscreen" in request.data:
        euscreen = request.data["euscreen"]
    else:
        return Response({"message": "specific video must be selected"})

    try:
        video = Video.objects.get(euscreen=euscreen)
    except Video.DoesNotExist:
        return Response({"message": "video does not exist"})

    user_content_score = UserContentScore.objects.filter(user_id=user.id).order_by('term_id')

    num_terms = Term.objects.count()

    # Force evaluate queryset for fast .score
    len(user_content_score)
    user_vector = [None] * num_terms

    for ii in range(num_terms):
        user_vector[ii] = float(user_content_score[ii].score)

    enrichments_list = enrichments_recommendation(user_vector, video.id)

    return Response({"enrichments": enrichments_list})
