from ..models import Term
from ..models import Video, VideoContentScore

from .cosine_similarity import *

import operator


# TODO optimize for speed
def video_recommendation(user_vector, videos_list, num_req_videos):

    # if user is new, use 0.1 as profile to avoid division by zero
    # TODO check better way to propose to new users
    if user_vector == [0]*len(user_vector):
        user_vector = [0.1]*len(user_vector)

    results_content = user_video_similarity(user_vector, videos_list)
    # TODO collaborative filtering

    sorted_results = sorted(results_content.items(), key=operator.itemgetter(1), reverse=True)
    sorted_results = sorted_results[0:num_req_videos]

    recommended_videos = []
    for result in sorted_results:
        recommended_videos.append(tuple([Video.objects.get(id=result[0]).euscreen, result[1]]))

    return recommended_videos


def user_video_similarity(user_vector, videos_list):

    num_terms = Term.objects.count()

    # if video_list is not empty search only on those videos, else search on all video database
    if videos_list:
        videos = Video.objects.filter(euscreen__in=videos_list)
    else:
        videos = Video.objects.all()

    video_content_scores = VideoContentScore.objects.filter(video__in=videos)

    # Force evaluate queryset for fast .score
    len(video_content_scores)

    video_vectors = {}
    for item in video_content_scores:

        # term ids start from 1 while term vector indexing starts from 0
        term_index = item.term_id-1

        if item.video_id in video_vectors:
            video_vectors[item.video_id][term_index] = float(item.score)
        else:
            video_vectors[item.video_id] = [None]*num_terms
            video_vectors[item.video_id][term_index] = float(item.score)

    similarity = {}

    for video_id, video_vector in video_vectors.items():
        similarity[video_id] = euclidean_similarity(user_vector, video_vector)

    return similarity
