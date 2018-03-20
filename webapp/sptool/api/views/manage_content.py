from rest_framework.response import Response
from rest_framework.decorators import api_view

from pathlib import Path

import gensim
from gensim.models import Doc2Vec

from ..models import Video, Term, VideoContentScore, VideoEnrichments
from ..models import Enrichment, EnrichmentContentScore

@api_view(['POST'])
def import_video(request, *args, **kwargs):

    if "video" in request.data:
        item = request.data["video"]
    else:
        return Response({"message": "No video provided for import"})

    euscreen = item["shared_id"]
    genre = item["genre"] if 'genre' in item else ""
    topic = item["topic"] if 'topic' in item else ""
    title = item["title"]
    geographical_coverage = item["geographical_coverage"] if 'geographical_coverage' in item else ""
    thesaurus_terms = item["thesaurus_terms"] if 'thesaurus_terms' in item else ""
    summary = item["description"]
    duration = item["duration"]

    source = item["source"] if 'source' in item else ""
    path = item["path"] if 'path' in item else ""
    tags = item["tags"] if 'tags' in item else ""
    annotations = item["annotations"] if 'annotations' in item else ""
    annotations_list = []

    if annotations:
        objects = annotations["objectdetection"] if 'objectdetection' in annotations else ""
        for object in objects:
            annotations_list.append(object["class"])

        faces = annotations["facedetection"] if 'facedetection' in annotations else ""
        for face in faces:
            annotations_list.append(face["face"])

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
            duration=duration,
            source=source,
            path=path,
            tags=tags,
            annotations=','.join(annotations_list)
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
            duration=duration,
            source=source,
            path=path,
            tags=tags,
            annotations=','.join(annotations_list)
        )

    try:
        score_video(euscreen)
    except FileNotFoundError:
        return Response({"message": "Model for scoring not found"})

    return Response({"message": "Imported \'%s\' video" % title})

@api_view(['POST'])
def delete_videos(request, *args, **kwargs):

    if "videos" in request.data:
        items = request.data["videos"]
    else:
        return Response({"message": "No videos provided for deletion"})

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


@api_view(['POST'])
def import_enrichments(request, *args, **kwargs):

    if "Items" in request.data:
        req = request.data["Items"][0]
    else:
        return Response({"message": "No enrichments provided for import"})

    items = req["marker"]

    project_id = req["pid"]
    euscreen = req["mcssruid"]
    video = Video.objects.get(euscreen=euscreen)

    for item in items:
        enrichment_id = item["options"]["modelOptions"]['1']['2']['v']
        name = item["options"]["modelOptions"]['1']['1']['v']

        if '2' in item["options"]["modelOptions"]:
            if '1' in item["options"]["modelOptions"]['2']:
                if 'v' in item["options"]["modelOptions"]['2']['1']:
                    title = item["options"]["modelOptions"]['2']['1']['v']
                else:
                    title = ""
            else:
                title = ""
        else:
            title = ""
        overlay_title = item["options"]["modelOptions"]['1']['8']['v'] if '8' in item["options"]["modelOptions"]['1'] else ""
        overlay_text_description = item["options"]["modelOptions"]['1']['9']['v'] if '9' in item["options"]["modelOptions"]['1'] else ""

        enrichment = Enrichment.objects.filter(enrichment_id=enrichment_id)
        if not enrichment.exists():
            enrichment = Enrichment(
                enrichment_id=enrichment_id,
                name=name,
                title=title,
                overlay_title=overlay_title,
                overlay_text_description=overlay_text_description
            )
            enrichment.save()

        else:
            enrichment.update(
                enrichment_id=enrichment_id,
                name=name,
                title=title,
                overlay_title=overlay_title,
                overlay_text_description=overlay_text_description
            )
            enrichment = enrichment[0]

            print(enrichment)

        for position in item["positions"]:
            x = position["bp"]["x"]
            y = position["bp"]["y"]
            start_time = position["b"]
            end_time = position["e"]

            video_enrichment = VideoEnrichments.objects\
                .filter(video_id=video.id)\
                .filter(enrichment_id=enrichment.id)\
                .filter(project_id=project_id)\
                .filter(x=x)\
                .filter(y=y)\
                .filter(start_time=start_time)\
                .filter(end_time=end_time)
            if video_enrichment.exists():
                pass
            else:
                video_enrichment = VideoEnrichments(
                    video_id=video.id,
                    enrichment_id=enrichment.id,
                    project_id=project_id,
                    x=x,
                    y=y,
                    start_time=start_time,
                    end_time=end_time
                )

                video_enrichment.save()

        try:
            score_enrichment(enrichment_id)
        except FileNotFoundError:
            return Response({"message": "Model for scoring not found"})

    return Response({"message": "Imported %d enrichments" % len(items)})

@api_view(['POST'])
def delete_enrichments(request, *args, **kwargs):

    if "enrichments" in request.data:
        items = request.data["enrichments"]
    else:
        return Response({"message": "No enrichments provided for deletion"})

    ii = 0
    for item in items:
        enrichment_id = item["enrichment_id"]

        enrichment = Enrichment.objects.filter(enrichment_id=enrichment_id)
        if not enrichment.exists():
            continue
        else:
            enrichment.delete()
            ii += 1

    return Response({"message": "Removed %d enrichments" % ii})

@api_view(['POST'])
def delete_enrichments_on_videos(request, *args, **kwargs):

    if "videos" in request.data:
        items = request.data["videos"]
    else:
        return Response({"message": "No videos provided for enrichment deletion"})

    ii = 0
    for item in items:
        euscreen = item["shared_id"]

        video = Video.objects.filter(euscreen=euscreen)
        if not video.exists():
            continue
        else:
            enrichments = VideoEnrichments.objects.filter(video=video)
            enrichments.delete()
            ii += 1

    return Response({"message": "Removed all enrichments on %d videos" % ii})

def score_enrichment(enrichment_id):
    model_path = "/srv/sptool/api/management/commands/data_files/doc2vec.model"
    my_file = Path(model_path)

    if my_file.is_file():
        pass
    else:
        raise FileNotFoundError("Model for scoring not found")

    model = Doc2Vec.load(model_path)

    terms_list = Term.objects.all()
    enrichment = Enrichment.objects.get(enrichment_id=enrichment_id)

    data = enrichment.name + " " + \
           enrichment.title + " " + \
           enrichment.overlay_title + " " + \
           enrichment.overlay_text_description

    enrichment_tokens = gensim.utils.simple_preprocess(data)

    for term in terms_list:

        term_tokens = gensim.utils.simple_preprocess(term.long_name)

        similarity = model.docvecs.similarity_unseen_docs(model, term_tokens, enrichment_tokens)
        similarity = similarity if similarity > 0 else 0

        enrichment_score = EnrichmentContentScore.objects.filter(enrichment_id=enrichment.id).filter(term_id=term.id)
        if enrichment_score.exists():
            enrichment_score.update(score=similarity)
        else:
            scoring = EnrichmentContentScore(
                enrichment_id=enrichment.id,
                term_id=term.id,
                score=similarity
            )
            scoring.save()

    return