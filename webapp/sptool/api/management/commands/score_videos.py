from django.core.management.base import BaseCommand
from ...models import Video, VideoContentScore
from ...models import Term

from pathlib import Path
from os import listdir
import sys

import gensim
from gensim.models import Doc2Vec


class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield gensim.models.doc2vec.LabeledSentence(words=doc.split(), tags=[self.labels_list[idx]])


class Command(BaseCommand):
    def handle(self, *args, **options):

        model_path = "./srv/sptool/api/management/commands/data_files/doc2vec.model"
        my_file = Path(model_path)

        if my_file.is_file():
            print("Using model from file")

        else:
            print("Creating model")

            docLabels = []
            docLabels = [f for f in listdir('./srv/sptool/api/management/commands/data_files/video_txts') if
                         f.endswith('.txt')]

            if docLabels == []:
                print("Error! There are no txt files")
                sys.exit()

            data = []

            for doc in docLabels:
                with open("./srv/sptool/api/management/commands/data_files/video_txts/" + doc, 'r') as fout:
                    data.append(fout.read())

            # TODO Data has \n inside. Check if it matters
            # TODO remove stopwords

            it = LabeledLineSentence(data, docLabels)

            # TODO check other parameters
            model = Doc2Vec(dm=0, size=300, window=5, negative=5, min_count=0, workers=4)

            model.build_vocab(it)

            # TODO check if shuffling data first helps (as suggested on gensim github)
            # TODO why does it have to model.train calls
            for epoch in range(10):
                model.train(it)
                model.alpha -= 0.002
                model.min_alpha = model.alpha
                model.train(it)

            # Import google_news word2vec on our model
            # TODO check if the word2vec from google news helps
            model.intersect_word2vec_format(
                './srv/sptool/api/management/commands/data_files/GoogleNews-vectors-negative300.bin', binary=True)

            model.save(model_path)

        model = Doc2Vec.load(model_path)

        terms_list = Term.objects.all()
        videos_list = Video.objects.all()

        num_of_videos = len(videos_list)

        for term in terms_list:

            print("Scoring for term: ", term.long_name)

            tokens = gensim.utils.simple_preprocess(term.long_name)
            new_doc_vec = model.infer_vector(tokens)

            # TODO check if there exists another api call that doesn't rank (for efficiency)
            similarities = model.docvecs.most_similar([new_doc_vec], topn=num_of_videos)
            for item in similarities:
                video_euscreen = item[0][:-4]
                video = videos_list.get(euscreen=video_euscreen)

                similarity = item[1] if item[1] > 0 else 0

                video_score = VideoContentScore.objects.filter(video_id=video.id).filter(term_id=term.id)
                if video_score.exists():
                    video_score.update(score=similarity)
                else:
                    scoring = VideoContentScore(
                        video_id=video.id,
                        term_id=term.id,
                        score=similarity
                    )
                    scoring.save()

        print("Done scoring!")
