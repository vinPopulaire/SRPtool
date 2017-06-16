from api.models import Term
from api.models import Enrichment, VideoEnrichments, EnrichmentContentScore

from .cosine_similarity import cosine_similarity

import operator


def top_enrichments_recommendation(user_vector, video_id, num_req_enrichments):

    results_content = user_enrichment_similarity(user_vector, video_id)

    # TODO collaborative filtering

    sorted_results = sorted(results_content.items(), key=operator.itemgetter(1), reverse=True)
    sorted_results = sorted_results[0:num_req_enrichments]

    recommended_enrichments = []
    for result in sorted_results:
        recommended_enrichments.append(tuple([Enrichment.objects.get(id=result[0]).enrichment_id, result[1]]))

    return recommended_enrichments


def user_enrichment_similarity(user_vector, video_id):

    num_terms = Term.objects.count()

    enrichments = VideoEnrichments.objects.filter(video_id=video_id)

    similarity = {}
    for enrichment in enrichments:
        enrichment_id = enrichment.enrichment_id
        enrichment_content_score = EnrichmentContentScore.objects.filter(enrichment=enrichment_id).order_by('term_id')

        # Force evaluate queryset for fast .score
        len(enrichment_content_score)
        enrichment_vector = [None]*num_terms

        for jj in range(num_terms):
            enrichment_vector[jj] = float(enrichment_content_score[jj].score)

        similarity[enrichment_id] = cosine_similarity(user_vector, enrichment_vector)

    return similarity
