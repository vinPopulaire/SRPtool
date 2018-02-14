import math


def cosine_similarity(vector_1, vector_2):

    num_terms = len(vector_1)

    numerator = 0
    sum_a = 0
    sum_b = 0

    for ii in range(num_terms):
        score_1 = vector_1[ii]
        score_2 = vector_2[ii]

        numerator += score_1*score_2
        sum_a += math.pow(score_1, 2)
        sum_b += math.pow(score_2, 2)

    similarity = numerator / (math.sqrt(sum_a)*math.sqrt(sum_b))

    return similarity

def euclidean_similarity(vector_1, vector_2):

    similarity = 1/(1 + euclidean_distance(vector_1, vector_2))

    return similarity

def euclidean_distance(vector_1, vector_2):

    num_terms = len(vector_1)
    sum_a = 0

    for ii in range(num_terms):
        score_1 = vector_1[ii]
        score_2 = vector_2[ii]

        sum_a += math.pow((score_1 - score_2),2)

    distance  = math.sqrt(sum_a)

    return distance