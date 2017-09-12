from collections import defaultdict

from api.models import Term
from api.models import Enrichment, VideoEnrichments, EnrichmentContentScore

from .cosine_similarity import cosine_similarity

import operator


def enrichments_recommendation(user_vector, video_id):

    # if user is new, use 0.1 as profile to avoid division by zero
    # TODO check better way to propose to new users
    if user_vector == [0] * len(user_vector):
        user_vector = [0.1] * len(user_vector)

    enrichments = VideoEnrichments.objects.filter(video_id=video_id)

    # keep enrichments that appear on the same time in a dictionary of lists
    dict_enrichments = defaultdict(list)
    for enrichment in enrichments:
        time = enrichment.time
        dict_enrichments[time].append(enrichment)

    # TODO it would be better if we had a unique id for each annotation to find which enrichments are on the same
    # annotation

    # check if enrichments that appear on the same time are on the same annotation
    recommended_enrichments = []
    for key, candidate_enrichments in dict_enrichments.items():

        # keep track if enrichment is already processed (if it was on the same object to an other one)
        checked_enrichments = set()
        for enrichment in candidate_enrichments:
            enrichment_id = enrichment.enrichment_id

            if enrichment_id in checked_enrichments:
                continue

            similarity = enrichment_similarity(user_vector, enrichment_id)

            # ATTENTION if tuple is changed, the index in the lambda function for sorting the tuples must also change
            simultaneous_enrichments = [tuple([key, Enrichment.objects.get(id=enrichment_id).enrichment_id, similarity])]
            checked_enrichments.add(enrichment_id)

            for tmp_enrichment in candidate_enrichments:
                tmp_enrichment_id = tmp_enrichment.enrichment_id

                if tmp_enrichment_id in checked_enrichments:
                    continue

                if enrichment.height == tmp_enrichment.height \
                        and enrichment.width == tmp_enrichment.width \
                        and enrichment.x_min == tmp_enrichment.x_min \
                        and enrichment.y_min == tmp_enrichment.y_min:

                    similarity = enrichment_similarity(user_vector, tmp_enrichment_id)

                    simultaneous_enrichments.append(
                        tuple([key, Enrichment.objects.get(id=tmp_enrichment_id).enrichment_id, similarity]))
                    checked_enrichments.add(tmp_enrichment_id)

            # ATTENTION if tuple is changed, the index in the lambda function for sorting the tuples must also change
            simultaneous_enrichments = sorted(simultaneous_enrichments, key=lambda x: x[2], reverse=True)
            recommended_enrichments.append(simultaneous_enrichments)

    return recommended_enrichments


def enrichment_similarity(user_vector, enrichment_id):

    num_terms = Term.objects.count()

    enrichment_content_score = EnrichmentContentScore.objects.filter(enrichment=enrichment_id).order_by('term_id')

    # Force evaluate queryset for fast .score
    len(enrichment_content_score)
    enrichment_vector = [None] * num_terms

    for jj in range(num_terms):
        enrichment_vector[jj] = float(enrichment_content_score[jj].score)

    similarity = cosine_similarity(user_vector, enrichment_vector)

    return similarity
