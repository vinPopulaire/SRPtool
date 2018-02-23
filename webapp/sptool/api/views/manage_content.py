from rest_framework.response import Response
from rest_framework.decorators import api_view

from pathlib import Path

import gensim
from gensim.models import Doc2Vec

from ..models import Video, Term, VideoContentScore

@api_view(['POST'])
def import_videos(request, *args, **kwargs):

    if "videos" in request.data:
        items = request.data["videos"]
    else:
        return Response({"message": "No videos provided for import"})

    for item in items:
        euscreen = item["shared_id"]
        genre = item["genre"]
        topic = item["topic"]
        title = item["title"]
        geographical_coverage = item["geographical_coverage"]
        thesaurus_terms = item["thesaurus_terms"]
        summary = item["summary"]
        duration = item["duration"]

        video = Video.objects.filter(euscreen=euscreen)
        if not video.exists():
            video = Video(
                euscreen=euscreen,
                genre=genre,
                topic=topic,
                title=title,
                geographical_coverage=geographical_coverage,
                thesaurus_terms=thesaurus_terms,
                summary=summary,
                duration=duration
            )
            video.save()

        else:
            video.update(
                genre=genre,
                topic=topic,
                title=title,
                geographical_coverage=geographical_coverage,
                thesaurus_terms=thesaurus_terms,
                summary=summary,
                duration=duration
            )

        try:
            score_video(euscreen)
        except FileNotFoundError:
            return Response({"message": "Model for scoring not found"})

    return Response({"message": "Imported %d videos" % len(items)})

@api_view(['POST'])
def delete_videos(request, *args, **kwargs):

    if "videos" in request.data:
        items = request.data["videos"]
    else:
        return Response({"message": "No videos provided for import"})

    ii = 0
    for item in items:
        euscreen = item["shared_id"]

        video = Video.objects.filter(euscreen=euscreen)
        if not video.exists():
            continue
        else:
            video.delete()
            ii += 1

    return Response({"message": "Removed %d videos" % ii})

def score_video(euscreen):
    model_path = "/srv/sptool/api/management/commands/data_files/doc2vec.model"
    my_file = Path(model_path)

    if my_file.is_file():
        pass
    else:
        raise FileNotFoundError("Model for scoring not found")

    model = Doc2Vec.load(model_path)

    terms_list = Term.objects.all()
    video = Video.objects.get(euscreen=euscreen)

    data = video.title + " " + \
           video.summary + " " + \
           video.genre + " " + \
           video.geographical_coverage + " " + \
           video.topic + " " + \
           video.thesaurus_terms

    video_tokens = gensim.utils.simple_preprocess(data)

    for term in terms_list:

        term_tokens = gensim.utils.simple_preprocess(term.long_name)

        similarity = model.docvecs.similarity_unseen_docs(model, term_tokens, video_tokens)
        similarity = similarity if similarity > 0 else 0

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

    return