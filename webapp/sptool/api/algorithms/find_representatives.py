from django.db.models import Max

from ..models import User, UserContentScore
from ..models import Term

from sklearn.cluster import KMeans
import numpy as np


def find_representatives(request):

    # get all users
    users = User.objects.all()

    # filter based on request
    if 'gender_id' in request.data:
        users = users.filter(gender_id=request.data["gender_id"])

    if 'age_id' in request.data:
        users = users.filter(age_id=request.data["age_id"])

    if 'education_id' in request.data:
        users = users.filter(education_id=request.data["education_id"])

    if 'occupation_id' in request.data:
        users = users.filter(occupation_id=request.data["occupation_id"])

    if 'country_id' in request.data:
        users = users.filter(country_id=request.data["country_id"])

    # TODO filter based on interests

    # remove users with no profile yet
    for user in users:
        max_score = float(UserContentScore.objects.filter(user=user).aggregate(Max('score'))['score__max'])
        if max_score == 0:
            users = users.exclude(id=user.id)

    if not users:
        # return empty list if there is no information on the target group
        representatives = []
        return representatives

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
        kmeans = KMeans(n_clusters=5, random_state=0).fit(x)
        clusterheads = kmeans.cluster_centers_
    except ValueError:
        # if clusters are more than the samples
        clusterheads = x

    representatives = clusterheads.tolist()

    return representatives
