from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework_api_key.permissions import HasAPIAccess

from ..models import User, Video, VideoWatched, VideoInteractions
from ..models import Action
from ..models import Enrichment


@api_view(['POST'])
@permission_classes((HasAPIAccess, ))
def user_watch(request, username, *args, **kwargs):

    euscreen = request.data["euscreen"]

    user = User.objects.get(username=username)
    video = Video.objects.get(euscreen=euscreen)

    already_watched = VideoWatched.objects.filter(user_id=user.id).filter(video_id=video.id)

    if already_watched:
        message = "user has already watched the video"
    else:
        video_watched = VideoWatched(
                user_id=user.id,
                video_id=video.id,
                liked=0
                )
        video_watched.save()
        message = "video watch saved"

    return Response({"result": "success", "message": message})


@api_view(['POST'])
@permission_classes((HasAPIAccess, ))
def user_actions(request, username, *args, **kwargs):

    euscreen = request.data["euscreen"]
    action_type = request.data["action"]

    user = User.objects.get(username=username)
    video = Video.objects.get(euscreen=euscreen)
    action = Action.objects.get(action=action_type)

    video_watched = VideoWatched.objects.filter(user_id=user.id).filter(video_id=video.id)

    if video_watched:
        message = store_video_interaction(video_watched[0], action, request)
    else:
        video_watched = VideoWatched(
            user_id=user.id,
            video_id=video.id,
            liked=0
        )
        video_watched.save()
        print("Video watch saved")
        message = store_video_interaction(video_watched, action, request)

    return Response({"result": "success", "message": message})


def store_video_interaction(video_watched, action, request):

    # TODO Cannot start again if already playing
    if action.id == 1:
        video_start_time = int(request.data["time"])

        interaction = VideoInteractions(
                video_watched_id=video_watched.id,
                action_id=action.id,
                video_time=video_start_time
                )
        interaction.save()
        message = "video started"

    # TODO Cannot stop if it hasn't started playing yet
    elif action.id == 2:
        video_start_time = VideoInteractions.objects.filter(video_watched_id=video_watched.id,action_id=1).last().video_time
        video_stop_time = int(request.data["time"])
        time_playing = video_stop_time - video_start_time
        duration = int(request.data["duration"])
        weight = float(time_playing)/duration

        interaction = VideoInteractions(
                video_watched_id=video_watched.id,
                action_id=action.id,
                video_time=video_stop_time,
                weight=weight
                )
        interaction.save()
        message = "video stopped"

    # TODO Cannot click enrichment again if it was clicked and not yet computed
    elif action.id == 3:
        enrichment_id = Enrichment.objects.get(enrichment_id=request.data["enrichment_id"]).id

        interaction = VideoInteractions(
                video_watched_id=video_watched.id,
                action_id=action.id,
                content_id=enrichment_id
                )
        interaction.save()
        message = "enrichment clicked"

    elif action.id == 4:
        # enrichment_id = Advertisement.objects.get(enrichment_id=request.data["enrichment_id"]).id

        # interaction = VideoInteractions(
        #         video_watched_id=video_watched.id,
        #         action_id=action.id,
        #         content_id=enrichment_id
        #         )
        # interaction.save()
        message = "advertisement clicked"

    elif action.id == 5:
        enrichment_id = Enrichment.objects.get(enrichment_id=request.data["enrichment_id"]).id

        interaction = VideoInteractions(
                video_watched_id=video_watched.id,
                action_id=action.id,
                content_id=enrichment_id
                )
        interaction.save()
        message = "enrichment shared"

    elif action.id == 6:
        explicit_rf = int(request.data["value"])

        if explicit_rf in [-1, 0, 1]:
            video_interaction = VideoInteractions.objects.filter(computed=False).filter(video_watched_id=video_watched.id).filter(action_id='6')

            if video_interaction:
                video_interaction[0].explicit_rf = explicit_rf
                video_interaction[0].save()
            else:
                interaction = VideoInteractions(
                        video_watched_id=video_watched.id,
                        action_id=action.id,
                        explicit_rf=explicit_rf
                        )
                interaction.save()

                video_watched.liked = explicit_rf
                video_watched.save()

            message = "explicit feedback considered"

        else:
            message = "not valid explicit feedback"

    else:
        message = "Not a valid action"

    return message
