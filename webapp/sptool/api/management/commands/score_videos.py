from django.core.management.base import BaseCommand
from ...models import Video, VideoContentScore
from ...models import Term

from pathlib import Path

import gensim
from gensim.models import KeyedVectors


class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield gensim.models.doc2vec.LabeledSentence(words=doc.split(), tags=[self.labels_list[idx]])


class Command(BaseCommand):
    def handle(self, *args, **options):

        model_path = "/srv/sptool/api/management/commands/data_files/word2vec.txt"
        my_file = Path(model_path)

        if my_file.is_file():
            pass
        else:
            raise FileNotFoundError("Model for scoring not found")

        print("Loading model")
        model = KeyedVectors.load_word2vec_format(model_path)
        print("Model loaded")

        terms_list = Term.objects.all()
        videos_list = Video.objects.all()

        num_videos = 1

        for video in videos_list:

            data = video.title + " " + \
                   video.topic + " " + \
                   video.genre + " " + \
                   video.thesaurus_terms + " " + \
                   video.tags + " " + \
                   video.annotations

            video_tokens = gensim.utils.simple_preprocess(data)

            for term in terms_list:

                # simple_preprocess returns a list with all tokens (just one in our case)
                term_token = gensim.utils.simple_preprocess(term.term)[0]

                # we will keep maximum similarity because it seems to provide clearer results
                # average similarity can also be considered
                max_similarity = 0
                for video_token in video_tokens:
                    # calculate similarity. If word does not exist in model, skip it
                    try:
                        similarity = model.wv.similarity(video_token, term_token)
                    except KeyError:
                        continue
                    if max_similarity < similarity:
                        max_similarity = similarity
                    max_similarity = similarity if max_similarity < similarity else max_similarity
                max_similarity = max_similarity if max_similarity > 0 else 0

                video_score = VideoContentScore.objects.filter(video_id=video.id).filter(term_id=term.id)
                if video_score.exists():
                    video_score.update(score=max_similarity)
                else:
                    scoring = VideoContentScore(
                        video_id=video.id,
                        term_id=term.id,
                        score=max_similarity
                    )
                    scoring.save()

            num_videos += 1
            if num_videos%50 == 0:
                print("%d videos scored!" % num_videos)

        print("Done scoring!")
