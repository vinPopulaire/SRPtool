from django.db.models import Max

from ..models import User, UserContentScore
from ..models import Term

from sklearn.cluster import KMeans
import numpy as np
from collections import Counter


def get_starting_vector(user):

    # get all users except the one in question
    users = User.objects.all().exclude(id=user.id)

    # order matters on the filtering (3 first play a more important role)
    demographics_list = ['gender_id','age_id','country_id','education_id','occupation_id']

    # get users that have the same demographics
    for demographic in demographics_list:

        kwargs = {
            demographic:getattr(user, demographic)
        }

        tmp_users = users.filter(**kwargs)
        # if no such user exists, skip the demographic
        if not tmp_users:
            continue
        users = tmp_users

    # remove users with no profile yet
    # TODO maybe remove since now the users don't start with a zero vector
    for user in users:
        max_score = float(UserContentScore.objects.filter(user=user).aggregate(Max('score'))['score__max'])
        if max_score == 0:
            users = users.exclude(id=user.id)

    x = np.array([])
    for user in users:
        user_id = user.id
        num_terms = Term.objects.count()

        user_content_score = UserContentScore.objects.filter(user_id=user_id).order_by('term_id')

        # Force evaluate queryset for fast .score
        len(user_content_score)
        user_vector = [None] * num_terms

        for ii in range(num_terms):
            user_vector[ii] = float(user_content_score[ii].score)

        if x.size:
            # append user_vector as an array and don't flatten
            x = np.append(x, [user_vector], axis=0)
        else:
            x = np.array([user_vector])

    # TODO check DBscan
    # TODO PCA to decrease dimensions for fixing curse of dimensionality
    # TODO find optimum number of clusters
    try:
        kmeans = KMeans(n_clusters=2, random_state=0).fit(x)
        clusterheads = kmeans.cluster_centers_
        num_of_members = Counter(kmeans.labels_)
    except ValueError:
        # if clusters are more than the samples
        # put each sample as a cluster
        # create a list of number of members with one member on each cluster
        clusterheads = x
        num_of_members = Counter(range(len(clusterheads)))

    # get the cluster with the most members
    biggest_cluster = num_of_members.most_common(1)[0][0]

    cluster_vector = clusterheads[biggest_cluster]

    return cluster_vector

