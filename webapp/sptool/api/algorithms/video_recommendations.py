from ..models import Term
from ..models import Video, VideoContentScore
from ..models import UserContentScore
from ..models import Friend

from .similarities import *

import operator


# TODO optimize for speed
def video_recommendation(user, videos_list, num_req_videos):
    # TODO move access to videos in this function so that it is only accessed one for multiple users

    user_vector = user.get_user_vector()
    user_id = user.id

    # if user is new, use 0.1 as profile to avoid division by zero
    # TODO check better way to propose to new users
    if user_vector == [0]*len(user_vector):
        user_vector = [0.1]*len(user_vector)

    results_content = user_video_similarity(user_vector, videos_list)
    results_collaborative = collaborative_filtering(user_vector, user_id, videos_list)

    final_recommendations = {}
    if results_collaborative:
        for key, value in results_content.items():
            final_recommendations[key] = 0.8*results_content[key] + 0.2*results_collaborative[key]

    else:
        final_recommendations = results_content

    sorted_results = sorted(final_recommendations.items(), key=operator.itemgetter(1), reverse=True)
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


def collaborative_filtering(user_vector, user_id, videos_list):

    # number of friends to consider on collaborative filtering
    kk = 3

    num_terms = Term.objects.count()

    friends = Friend.objects.filter(user_id=user_id)

    friends_list = []
    for friend in friends:
        friends_list.append(friend.friend_id)

    # This list contains the users that are not the user's friends
    friend_content_scores = UserContentScore.objects.filter(user_id__in=friends_list)

    # Force evaluate queryset for fast .score
    len(friend_content_scores)

    friend_vectors = {}
    for item in friend_content_scores:

        # term ids start from 1 while term vector indexing starts from 0
        term_index = item.term_id - 1

        if item.user_id in friend_vectors:
            friend_vectors[item.user_id][term_index] = float(item.score)
        else:
            friend_vectors[item.user_id] = [None] * num_terms
            friend_vectors[item.user_id][term_index] = float(item.score)

    similarity = {}

    for friend_id, friend_vector in friend_vectors.items():
        similarity[friend_id] = euclidean_similarity(user_vector, friend_vector)

    closest_friends = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
    closest_friends = closest_friends[0:kk]

    if not closest_friends:
        return []

    num_closest_friends = len(closest_friends)

    if videos_list:
        videos = Video.objects.filter(euscreen__in=videos_list)
    else:
        videos = Video.objects.all()

    # create structure to store the mean of closest friends
    similarity = {}
    for video in videos:
        similarity[video.id] = 0

    # loop through friends and calculate their mean on every video
    for friend in closest_friends:

        friend_id = friend[0]
        friend_similarity = friend[1]
        friend_vector = friend_vectors[friend_id]

        friend_result_content = user_video_similarity(friend_vector, videos_list)

        # weight each score of friend by multiplying the similarity the friend has with the user
        for key, value in friend_result_content.items():
            similarity[key] = similarity[key] + (value/num_closest_friends)*friend_similarity

    return similarity