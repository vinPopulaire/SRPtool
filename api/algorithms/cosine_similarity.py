import math


def cosine_similarity(vector_1, vector_2):

    num_terms = len(vector_1)

    numerator = 0
    sumA = 0
    sumB = 0

    for ii in range(num_terms):
        score_1 = vector_1[ii]
        score_2 = vector_2[ii]

        numerator += score_1*score_2
        sumA += math.pow(score_1, 2)
        sumB += math.pow(score_2, 2)

    similarity = numerator / (math.sqrt(sumA)*math.sqrt(sumB))

    return similarity
