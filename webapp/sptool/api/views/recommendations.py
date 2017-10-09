from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..algorithms import video_recommendation, find_representatives
from ..algorithms import enrichments_recommendation
from ..models import User
from ..models import Video


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

    result = []
    for video in recommended_videos_list:
        result.append({
            "video": video[0],
            "similarity": video[1]
        })

    return Response({"videos": result})


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

        recommended_videos_list = video_recommendation(representatives[i], videos_list, num_req_videos)

        result = []
        for video in recommended_videos_list:
            result.append({
                "video": video[0],
                "similarity": video[1]
            })

        videos['representative %d' % (i + 1)] = result

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

    # list of all enrichments scored and batched if simultaneous
    enrichments_list = enrichments_recommendation(user_vector, video.id)

    if "num" in request.data:
        num_enrichments = int(request.data["num"])

        recommended_enrichments = []
        # insert first enrichment (best score) of the simultaneous ones to the list
        for enrichments in enrichments_list:
            recommended_enrichments.append(enrichments[0])

        recommended_enrichments = sorted(recommended_enrichments, key=lambda x: x[2], reverse=True)

        # checks the number of enrichments and if it is non zero, it returns the appropriate slice
        # else if it is zero, it returns all the recommended enrichments
        if num_enrichments != 0:
            recommended_enrichments = recommended_enrichments[0:num_enrichments]

    else:
        # TODO ERROR because of multiple enrichments, the dictionary later on is not created correctly
        recommended_enrichments = enrichments_list

    result = []
    for enrichment in recommended_enrichments:
        result.append({
            "frame": enrichment[0],
            "id": enrichment[1],
            "similarity": enrichment[2]
        })

    return Response({"enrichments": result})


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

            # checks the number of enrichments and if it is non zero, it returns the appropriate slice
            # else if it is zero, it returns all the recommended enrichments
            if num_enrichments != 0:
                recommended_enrichments = recommended_enrichments[0:num_enrichments]

        else:
            # TODO ERROR because of multiple enrichments, the dictionary later on is not created correctly
            recommended_enrichments = enrichments_list

        result = []
        for enrichment in recommended_enrichments:
            result.append({
                "frame": enrichment[0],
                "id": enrichment[1],
                "similarity": enrichment[2]
            })
        result_enrichments['representative %d' % (i + 1)] = result

    if representatives:
        response = Response(result_enrichments)
    else:
        response = Response({"message": "no information on target group"})

    return response
