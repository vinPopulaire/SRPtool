from api.models import User, UserContentScore
from api.models import Term
from api.models import Video, VideoContentScore

import math
import operator

# TODO optimize for speed

def video_recommendation(request, username):

    if "num" in request.data:
        num_req_videos = int(request.data["num"])
    else:
        num_req_videos = 10

    user = User.objects.get(username=username)

    results_content = user_content_similarity(user)

    sorted_results = sorted(results_content.items(), key=operator.itemgetter(1), reverse=True)

    sorted_results = sorted_results[0:num_req_videos]

    recommended_videos = [None]*num_req_videos
    for ii in range(num_req_videos):
        recommended_videos[ii] = Video.objects.get(id=sorted_results[ii][0]).euscreen
    return recommended_videos


def user_content_similarity(user):

    user_id = user.id
    num_terms = Term.objects.count()

    user_content_score = UserContentScore.objects.filter(user_id=user_id).order_by('term_id')

    # Force evaluate queryset for fast .score
    len(user_content_score)
    user_vector = [None]*num_terms

    for ii in range(num_terms):
        user_vector[ii] = user_content_score[ii].score

    videos = Video.objects.all()

    similarity = {}
    for video in videos:
        video_id = video.id
        video_content_score = VideoContentScore.objects.filter(video_id=video_id).order_by('term_id')

        # Force evaluate queryset for fast .score
        len(video_content_score)
        video_vector = [None]*num_terms

        for jj in range(num_terms):
            video_vector[jj] = video_content_score[jj].score

        similarity[video.id] = cosine_similarity(user_vector, video_vector)

    return similarity


def cosine_similarity(vector_1, vector_2):

    num_terms = len(vector_1)

    numerator = 0
    sumA = 0
    sumB = 0

    for ii in range(num_terms):
        score_1 = vector_1[ii]
        score_2 = vector_2[ii]

        numerator += score_1*score_2
        sumA += math.pow(score_1,2)
        sumB += math.pow(score_2,2)

    similarity = float(numerator) / (math.sqrt(sumA)+math.sqrt(sumB))

    return similarity
