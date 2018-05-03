from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..algorithms import video_recommendation, find_representatives
from ..algorithms import video_recommendation_to_target
from ..algorithms import enrichments_recommendation, enrichment_score
from ..algorithms import enrichments_recommendation_for_project
from ..algorithms import user_recommendation
from ..models import User
from ..models import Video, Enrichment, VideoEnrichments


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

    recommended_videos_list = video_recommendation(user, videos_list, num_req_videos)

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

    clusters = find_representatives(request)

    if clusters:

        # create json output of representatives with videos
        videos = {}
        i = 1
        for key, value in clusters.items():

            recommended_videos_list = video_recommendation_to_target(list(value["representative"]), videos_list, num_req_videos)

            result = []
            for video in recommended_videos_list:
                result.append({
                    "video": video[0],
                    "similarity": video[1],
                })

            videos['representative %d' % i] = {
                "videos": result,
                "num_of_members": value["num_of_members"]
            }
            i = i + 1

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
        recommended_enrichments = enrichments_list
        # Flatten to match the structure we have in the if statement
        recommended_enrichments = [item for items in recommended_enrichments for item in items]

    result = []
    for enrichment in recommended_enrichments:
        result.append({
            "start_time": enrichment[0],
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

    clusters = find_representatives(request)

    if clusters:

        # create json output of representatives with videos
        result_enrichments = {}
        i = 1
        for key,value in clusters.items():

            enrichments_list = enrichments_recommendation(list(value["representative"]), video.id)

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
                recommended_enrichments = enrichments_list
                # Flatten to match the structure we have in the if statement
                recommended_enrichments = [item for items in recommended_enrichments for item in items]

            result = []
            for enrichment in recommended_enrichments:
                result.append({
                    "start_time": enrichment[0],
                    "id": enrichment[1],
                    "similarity": enrichment[2]
                })

            result_enrichments['representative %d' % i] = {
                "enrichments": result,
                "num_of_members": value["num_of_members"]
            }
            i = i + 1

        response = Response(result_enrichments)
    else:
        response = Response({"message": "no information on target group"})

    return response


@api_view(['POST'])
def recommend_enrichments_to_target_for_IEVCT(request, *args, **kwargs):

    if "project_id" in request.data:
        project_id = request.data["project_id"]
    else:
        return Response({"message": "specific project must be selected"})

    # find mcssr_id because the IEVCT needs it
    video_id = VideoEnrichments.objects.filter(project_id=project_id)[0].video_id
    mcssruid = Video.objects.get(id=video_id).euscreen

    clusters = find_representatives(request)

    if clusters:

        # get results for the cluster with most members
        max_num = 0
        cluster_vector = []
        for key,value in clusters.items():
            if max_num < value["num_of_members"]:
                max_num = value["num_of_members"]
                cluster_vector = list(value["representative"])

        enrichments_list = enrichments_recommendation_for_project(cluster_vector, project_id)

        recommended_enrichments = []
        # insert first enrichment (best score) to the list for simultaneous enrichments
        for enrichments in enrichments_list:
            recommended_enrichments.append(enrichments[0])

        recommended_enrichments = sorted(recommended_enrichments, key=lambda x: x[2], reverse=True)

        result = []
        for recommended_enrichment in recommended_enrichments:

            enrichment_id = recommended_enrichment[1]
            enrichment = Enrichment.objects.get(enrichment_id=enrichment_id)
            # get the json for the first enrichment with the same name
            enrichment_json = VideoEnrichments.objects.filter(enrichment_id=enrichment.id).filter(project_id=project_id)[0].marker

            result.append(
                enrichment_json
            )

        result_enrichments = {
            "project_id": project_id,
            "mcssruid": mcssruid,
            "marker": result
        }

        response = Response(result_enrichments)
    else:
        response = Response({"message": "no information on target group"})

    return response


@api_view(['POST'])
def recommend_enrichment_from_set(request, username, *args, **kwargs):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": "user does not exist"})

    user_vector = user.get_user_vector()

    if "Items" in request.data:
        sets = request.data["Items"]
    else:
        return Response({"message": "specify some sets of enrichments"})

    max_similarity = 0
    max_URL = ""
    for set in sets:
        enrichments = set["marker"]
        url = set["source"]["url"]

        num = len(set["marker"])
        similarities = []

        for enrichment in enrichments:
            enrichment_id = enrichment["options"]["modelOptions"]['1']['2']['v']

            try:
                enrichment = Enrichment.objects.get(enrichment_id=enrichment_id)
            except Enrichment.DoesNotExist:
                return Response({"message": "enrichment \'%s\' does not exist" % enrichment_id})

            similarity = enrichment_score(user_vector, enrichment)
            similarities.append(similarity)

        # calculate average similarity of set
        avg_similarity = sum(similarities)/num

        if avg_similarity > max_similarity:
            max_similarity = avg_similarity
            max_URL = url

    result = max_URL

    return Response({"URL": result})


@api_view(['POST'])
def recommend_friends(request, username, *args, **kwargs):

    if "num" in request.data:
        num_req_friends = int(request.data["num"])
    else:
        num_req_friends = 5

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": "user does not exist"})

    user_vector = user.get_user_vector()
    user_id = user.id

    recommended_users_list = user_recommendation(user_vector, user_id, num_req_friends)

    result = []
    for user in recommended_users_list:
        result.append({
            "user": user[0],
            "similarity": user[1]
        })

    return Response({"users": result})