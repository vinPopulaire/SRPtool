from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.algorithms import video_recommendation, find_representatives
from api.algorithms import enrichments_recommendation
from api.models import User
from api.models import Video


@api_view(['POST'])
def recommend_videos(request, username, *args, **kwargs):

    if "num" in request.data:
        num_req_videos = int(request.data["num"])
    else:
        num_req_videos = 10

    if "videos" in request.data:
        videos_list = request.data["videos"].rstrip().split(",")
        # if it's an empty string make it empty array so that checks can be made later on correctly
        videos_list = [] if videos_list == [""] else videos_list
    else:
        videos_list = []

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": "user does not exist"})

    user_vector = user.get_user_vector()

    recommended_videos_list = video_recommendation(user_vector, videos_list, num_req_videos)

    return Response({"videos": recommended_videos_list})


@api_view(['POST'])
def recommend_videos_to_target(request, *args, **kwargs):

    if "num" in request.data:
        num_req_videos = int(request.data["num"])
    else:
        num_req_videos = 10

    if "videos" in request.data:
        videos_list = request.data["videos"].rstrip().split(",")
        # if it's an empty string make it empty array so that checks can be made later on correctly
        videos_list = [] if videos_list == [""] else videos_list
    else:
        videos_list = []

    representatives = find_representatives(request)

    # create json output of representatives with videos
    videos = {}
    for i in range(0, len(representatives)):

        videos['representative %d' % (i + 1)] = video_recommendation(representatives[i], videos_list, num_req_videos)

    if representatives:
        response = Response(videos)
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

    user_vector = user.get_user_vector()

    # list of all enrichments scored and batched if simultanious
    enrichments_list = enrichments_recommendation(user_vector, video.id)

    if "num" in request.data:
        num_enrichments = int(request.data["num"])

        recommended_enrichments = []
        # insert first enrichment (best score) of the simultaneous ones to the list
        for enrichments in enrichments_list:
            recommended_enrichments.append(enrichments[0])

        recommended_enrichments = sorted(recommended_enrichments, key=lambda x: x[2], reverse=True)
        recommended_enrichments = recommended_enrichments[0:num_enrichments]

    else:
        recommended_enrichments = enrichments_list

    return Response({"enrichments": recommended_enrichments})


@api_view(['POST'])
def recommend_enrichments_to_target(request, *args, **kwargs):

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
    result_enrichments = {}
    for i in range(0, len(representatives)):

        enrichments_list = enrichments_recommendation(representatives[i], video.id)

        if "num" in request.data:
            num_enrichments = int(request.data["num"])

            recommended_enrichments = []
            # insert first enrichment (best score) to the list for simultaneous enrichments
            for enrichments in enrichments_list:
                recommended_enrichments.append(enrichments[0])

            recommended_enrichments = sorted(recommended_enrichments, key=lambda x: x[2], reverse=True)
            recommended_enrichments = recommended_enrichments[0:num_enrichments]

        else:
            recommended_enrichments = enrichments_list

        # enrichments['representative %d' % (i + 1)] = recommended_enrichments
        result_enrichments['representative %d' % (i + 1)] = recommended_enrichments

    if representatives:
        response = Response(result_enrichments)
    else:
        response = Response({"message": "no information on target group"})

    return response
