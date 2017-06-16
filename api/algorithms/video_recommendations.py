from api.models import Term
from api.models import Video, VideoContentScore

from .cosine_similarity import cosine_similarity

import operator


# TODO optimize for speed
def video_recommendation(user_vector, num_req_videos):

    results_content = user_video_similarity(user_vector)
    # TODO collaborative filtering

    sorted_results = sorted(results_content.items(), key=operator.itemgetter(1), reverse=True)
    sorted_results = sorted_results[0:num_req_videos]

    recommended_videos = []
    for result in sorted_results:
        recommended_videos.append(tuple([Video.objects.get(id=result[0]).euscreen, result[1]]))

    return recommended_videos


def user_video_similarity(user_vector):

    num_terms = Term.objects.count()

    videos = Video.objects.all()

    similarity = {}
    for video in videos:
        video_content_score = VideoContentScore.objects.filter(video_id=video.id).order_by('term_id')

        # Force evaluate queryset for fast .score
        len(video_content_score)
        video_vector = [None]*num_terms

        for jj in range(num_terms):
            video_vector[jj] = float(video_content_score[jj].score)

        similarity[video.id] = cosine_similarity(user_vector, video_vector)

    return similarity