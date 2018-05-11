from ..models import UserContentScore
from ..models import VideoInteractions, VideoWatched
from ..models import Video, VideoContentScore
from ..models import User
from ..models import VideoEnrichments, EnrichmentContentScore
from ..models import Action


def update_prof(request, username):

    euscreen = request.data["euscreen"]

    video = Video.objects.get(euscreen=euscreen)
    user = User.objects.get(username=username)

    # list of actions performed on video from user and not yet computed
    video_watched = VideoWatched.objects.get(user=user, video=video)

    actions = VideoInteractions.objects.filter(computed=False).filter(video_watched=video_watched)

    # number of enrichments on video
    num_enrichments_on_video = VideoEnrichments.objects.filter(video=video).count()

    # set number of enrichments to 1 in order to avoid division by zero when video has no enrichments
    num_enrichments_on_video = num_enrichments_on_video if num_enrichments_on_video else 1

    # list of clicked enrichments
    clicked_enrichments = actions.filter(action_id=3)
    num_clicked_enrichments = len(clicked_enrichments)

    weight_clicked = num_clicked_enrichments / float(num_enrichments_on_video)

    # number of clicked ads
    clicked_ads = actions.filter(action_id=4)
    num_clicked_ads = len(clicked_ads)

    # TODO fix when we have ads on videos
    num_ads_on_video = 1
    weight_ads = num_clicked_ads / float(num_ads_on_video)

    # list of shared enrichments
    shared_enrichments = actions.filter(action_id=5)
    num_shared_enrichments = len(shared_enrichments)

    weight_shared = num_shared_enrichments / float(num_enrichments_on_video)

    # calculate k_denominator
    all_actions = Action.objects.all()

    # don't take into account importances when no enrichments or ads are present
    importances = []
    importances.append(all_actions.get(id=1).importance)
    importances.append(all_actions.get(id=2).importance)
    if num_enrichments_on_video > 1:
        importances.append(all_actions.get(id=3).importance)
    if num_ads_on_video > 1:
        importances.append(all_actions.get(id=4).importance)
    importances.append(all_actions.get(id=5).importance)
    importances.append(all_actions.get(id=6).importance)

    # old approach take into account all importances
    # importances = list(all_actions.values_list('importance', flat=True))

    k_denominator = float(sum(importances))

    # calculate k_nominator
    k_nominator = 0
    stop_actions = actions.filter(action_id=2)
    for stop_action in stop_actions:
        k_nominator += stop_action.weight*float(all_actions.get(id=2).importance)
    k_nominator += float(all_actions.get(id=3).importance)*weight_clicked \
                   + float(all_actions.get(id=4).importance)*weight_shared \
                   + float(all_actions.get(id=5).importance)*weight_ads

    explicit_rf = actions.filter(action_id=6)

    # TODO check if explicit_rf is the only thing that needs to be checked if it exists
    if explicit_rf:
        k_nominator += float(all_actions.get(id=6).importance)*explicit_rf[0].explicit_rf

    k = k_nominator / k_denominator

    k_negative = 0
    if k < 0:
        k_negative = 1
        print("\nuser didn't like the video and k = %f\n" % k)
        k = abs(k)

    # retrieve terms for given video
    video_terms = VideoContentScore.objects.filter(video=video)

    # update user score based on video terms
    for video_term in video_terms:
        term_id = video_term.term_id

        user_content_score = UserContentScore.objects.filter(user=user).get(term_id=term_id)
        old_value = float(user_content_score.score)

        # if k is negative we try to "push" the value away from the
        if clicked_enrichments and shared_enrichments:
            score = 0.8*float(video_term.score)
        elif clicked_enrichments or shared_enrichments:
            score = 0.9*float(video_term.score)
        else:
            score = float(video_term.score)
        if k_negative:
            value = (old_value - score) + old_value
        else:
            value = score

        # update user score based on enrichment terms
        for clicked_enrichment in clicked_enrichments:
            enrichment_term_score = EnrichmentContentScore.objects.filter(enrichment_id=clicked_enrichment.content_id).get(term_id=term_id)
            value += (0.1/num_clicked_enrichments)*float(enrichment_term_score.score)

        for shared_enrichment in shared_enrichments:
            enrichment_term_score = EnrichmentContentScore.objects.filter(enrichment_id=shared_enrichment.content_id).get(term_id=term_id)
            value += (0.1/num_shared_enrichments)*float(enrichment_term_score.score)

        # scale how much the new value is taken into account relatively to k (if 0.2*k)
        # k = 0 -> theta = 0.0
        # k = 1 -> theta = 0.2
        # 0 < k < 1 -> 0 < theta < 0.2
        theta = 0.5*k
        new_value = (1-theta)*old_value + theta*value

        # don't allow negative scores or bigger than 1
        new_value = max(new_value, 0)
        new_value = min(new_value, 1)

        user_content_score.score = new_value
        user_content_score.save()

    for action in actions:
        action.computed = True
        action.save()

    message = "user's profile is updated"

    return message
