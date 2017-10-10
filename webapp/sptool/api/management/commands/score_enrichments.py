from django.core.management.base import BaseCommand
from ...models import Enrichment, EnrichmentContentScore
from ...models import Term

from pathlib import Path
import sys

import gensim
from gensim.models import Doc2Vec


class Command(BaseCommand):

    def handle(self, *args, **options):

        model_path = "./srv/sptool/api/management/commands/data_files/doc2vec.model"
        my_file = Path(model_path)

        if my_file.is_file():
            print("Using model from file")

        else:
            print("Model not found")
            sys.exit()

        model = Doc2Vec.load(model_path)

        terms_list = Term.objects.all()
        enrichments_list = Enrichment.objects.all()

        for term in terms_list:

            print("Scoring for term: ", term.long_name)

            tokens_term = gensim.utils.simple_preprocess(term.long_name)

            for enrichment in enrichments_list:
                tokens_enrichment = gensim.utils.simple_preprocess(enrichment.description)
                similarity = model.docvecs.similarity_unseen_docs(model,tokens_term,tokens_enrichment)

                similarity = similarity if similarity>0 else 0

                enrichment_score = EnrichmentContentScore.objects.filter(enrichment_id=enrichment.id).filter(term_id=term.id)

                if enrichment_score.exists():
                    enrichment_score.update(score=similarity)
                else:
                    enrichment_score = EnrichmentContentScore(
                            enrichment_id=enrichment.id,
                            term_id=term.id,
                            score=similarity
                            )
                    enrichment_score.save()

        print("Done scoring enrichments!")
