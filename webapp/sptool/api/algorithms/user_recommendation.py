from ..models import Term
from ..models import Friend, User, UserContentScore

from .cosine_similarity import *

import operator

def user_recommendation(user_vector, user_id, num_req_videos):

    # if user is new, use 0.1 as profile to avoid division by zero
    # TODO check better way to propose to new users
    if user_vector == [0]*len(user_vector):
        user_vector = [0.1]*len(user_vector)

    # only content based recommendation on friends
    results_content = user_user_similarity(user_vector, user_id)

    sorted_results = sorted(results_content.items(), key=operator.itemgetter(1), reverse=True)
    sorted_results = sorted_results[0:num_req_videos]

    recommended_videos = []
    for result in sorted_results:
        recommended_videos.append(tuple([User.objects.get(id=result[0]).username, result[1]]))

    return recommended_videos


def user_user_similarity(user_vector, user_id):

    num_terms = Term.objects.count()

    friends = Friend.objects.filter(user_id=user_id)

    # Add the user's id in the list so that we don't recommend himself
    friends_list = [user_id]
    for friend in friends:
        friends_list.append(friend.friend_id)

    # This list contains the users that are not the user's friends
    friend_content_scores = UserContentScore.objects.exclude(user_id__in=friends_list)

    # Force evaluate queryset for fast .score
    len(friend_content_scores)

    friend_vectors = {}
    for item in friend_content_scores:

        # term ids start from 1 while term vector indexing starts from 0
        term_index = item.term_id-1

        if item.user_id in friend_vectors:
            friend_vectors[item.user_id][term_index] = float(item.score)
        else:
            friend_vectors[item.user_id] = [None]*num_terms
            friend_vectors[item.user_id][term_index] = float(item.score)

    similarity = {}

    for friend_id, friend_vector in friend_vectors.items():
        similarity[friend_id] = euclidean_similarity(user_vector, friend_vector)

    return similarity
