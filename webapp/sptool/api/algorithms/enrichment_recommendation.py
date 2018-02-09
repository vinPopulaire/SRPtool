from collections import defaultdict

from ..models import Term
from ..models import Enrichment, VideoEnrichments, EnrichmentContentScore

from .cosine_similarity import *


def enrichments_recommendation(user_vector, video_id):

    # if user is new, use 0.1 as profile to avoid division by zero
    # TODO check better way to propose to new users
    if user_vector == [0] * len(user_vector):
        user_vector = [0.1] * len(user_vector)

    # what enrichments are present in the video
    video_enrichments = VideoEnrichments.objects.filter(video_id=video_id)

    # information about the enrichments themselves
    enrichments = Enrichment.objects.filter(videoenrichments__in=video_enrichments)

    # score of the present enrichments
    enrichment_content_scores = EnrichmentContentScore.objects.filter(enrichment_id__in=enrichments)

    # Force evaluate queryset for fast .score
    len(enrichment_content_scores)

    num_terms = Term.objects.count()

    enrichment_vectors = {}
    for item in enrichment_content_scores:

        # term ids start from 1 while term vector indexing starts from 0
        term_index = item.term_id - 1

        if item.enrichment_id in enrichment_vectors:
            enrichment_vectors[item.enrichment_id][term_index] = float(item.score)
        else:
            enrichment_vectors[item.enrichment_id] = [None] * num_terms
            enrichment_vectors[item.enrichment_id][term_index] = float(item.score)

    # keep enrichments that appear on the same time in a dictionary of lists
    dict_enrichments = defaultdict(list)
    for enrichment in video_enrichments:
        time = enrichment.time
        dict_enrichments[time].append(enrichment)

    # TODO it would be better if we had a unique id for each annotation to find which enrichments are on the same
    # annotation

    # check if enrichments that appear on the same time are on the same annotation
    recommended_enrichments = []
    for time, candidate_enrichments in dict_enrichments.items():

        # keep track if enrichment is already processed (if it was on the same object to an other one)
        checked_enrichments = set()
        for enrichment in candidate_enrichments:
            enrichment_id = enrichment.enrichment_id

            if enrichment_id in checked_enrichments:
                continue

            similarity = enrichment_similarity(user_vector, enrichment_vectors[enrichment_id])

            # ATTENTION if tuple is changed, the index in the lambda function for sorting the tuples must also change
            simultaneous_enrichments = [tuple([time, Enrichment.objects.get(id=enrichment_id).enrichment_id, similarity])]
            checked_enrichments.add(enrichment_id)

            for tmp_enrichment in candidate_enrichments:
                tmp_enrichment_id = tmp_enrichment.enrichment_id

                if tmp_enrichment_id in checked_enrichments:
                    continue

                if enrichment.height == tmp_enrichment.height \
                        and enrichment.width == tmp_enrichment.width \
                        and enrichment.x_min == tmp_enrichment.x_min \
                        and enrichment.y_min == tmp_enrichment.y_min:

                    similarity = enrichment_similarity(user_vector, enrichment_vectors[tmp_enrichment_id])

                    simultaneous_enrichments.append(
                        tuple([time, Enrichment.objects.get(id=tmp_enrichment_id).enrichment_id, similarity]))
                    checked_enrichments.add(tmp_enrichment_id)

            # ATTENTION if tuple is changed, the index in the lambda function for sorting the tuples must also change
            simultaneous_enrichments = sorted(simultaneous_enrichments, key=lambda x: x[2], reverse=True)
            recommended_enrichments.append(simultaneous_enrichments)

    return recommended_enrichments


def enrichment_similarity(user_vector, enrichment_vector):

    similarity = euclidean_similarity(user_vector, enrichment_vector)

    return similarity
