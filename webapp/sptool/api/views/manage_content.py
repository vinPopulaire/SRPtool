from rest_framework.response import Response
from rest_framework.decorators import api_view

from pathlib import Path

import gensim
from gensim.models import KeyedVectors

from ..models import Video, Term, VideoContentScore, VideoEnrichments
from ..models import Enrichment, EnrichmentContentScore

from django.core.cache import cache
from decimal import *

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
    model_cache_key = "model_cache"
    model = cache.get(model_cache_key)

    if model is None:

        print("Importing model to cache")
        model_path = "/srv/sptool/api/management/commands/data_files/word2vec.txt"
        my_file = Path(model_path)

        if my_file.is_file():
            pass
        else:
            raise FileNotFoundError("Model for scoring not found")

        model = KeyedVectors.load_word2vec_format(model_path)
        cache.set(model_cache_key, model, None)

    terms_list = Term.objects.all()
    video = Video.objects.get(euscreen=euscreen)

    # IDEA split data in two so that similarity comes 0.5 from tags and 0.5 from the other
    # tags contribute using maximum similarity
    # other contribute using average similarity
    data = video.title + " " + \
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
                similarity = model.wv.similarity(video_token,term_token)
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

    enrichments_list = []
    for item in items:
        enrichment_id = item["options"]["modelOptions"]['1']['2']['v']
        enrichments_list.append(enrichment_id)
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

        # TODO find a way to update enrichments position (currently not possible)
        for position in item["positions"]:
            # cast float to Decimal because the SQL representation is in Decimal
            x = position["bp"]["x"]
            x = Decimal(str(round(x,2)))
            y = position["bp"]["y"]
            y = Decimal(str(round(y,2)))
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
                    end_time=end_time,
                    marker=item
                )

                video_enrichment.save()

    try:
        # score for the list of enrichments in order to open the model only once
        score_enrichments(enrichments_list)
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

@api_view(['POST'])
def delete_enrichments_on_project(request, *args, **kwargs):

    if "project_id" in request.data:
        project_id = request.data["project_id"]
    else:
        return Response({"message": "No project provided for enrichment deletion"})

    enrichments = VideoEnrichments.objects.filter(project_id=project_id)

    if enrichments.count() > 0:
        enrichments.delete()

        return Response({"message": "Deleted project " + project_id + " along with its enrichments"})
    else:
        return Response({"message": "The project doesn't exist in the database"})

def score_enrichments(enrichments_list):
    # load model once for all enrichments
    model_cache_key = "model_cache"
    model = cache.get(model_cache_key)

    if model is None:

        print("Importing model to cache")
        model_path = "/srv/sptool/api/management/commands/data_files/word2vec.txt"
        my_file = Path(model_path)

        if my_file.is_file():
            pass
        else:
            raise FileNotFoundError("Model for scoring not found")

        model = KeyedVectors.load_word2vec_format(model_path)

        cache.set(model_cache_key, model, None)

    for enrichment_id in enrichments_list:
        score_enrichment(enrichment_id, model)

def score_enrichment(enrichment_id, model):

    terms_list = Term.objects.all()
    enrichment = Enrichment.objects.get(enrichment_id=enrichment_id)

    # IDEA split data in two so that similarity comes 0.5 from tags and 0.5 from the other
    # tags contribute using maximum similarity
    # other contribute using average similarity
    data = enrichment.name + " " + \
           enrichment.title + " " + \
           enrichment.overlay_title + " " + \
           enrichment.overlay_text_description

    enrichment_tokens = gensim.utils.simple_preprocess(data)

    for term in terms_list:

        # simple_preprocess returns a list with all tokens (just one in our case)
        term_token = gensim.utils.simple_preprocess(term.term)[0]

        # we will keep maximum similarity because it seems to provide clearer results
        # average similarity can also be considered
        max_similarity = 0
        for enrichment_token in enrichment_tokens:
            # calculate similarity. If word does not exist in model, skip it
            try:
                similarity = model.wv.similarity(enrichment_token, term_token)
            except KeyError:
                continue
            if max_similarity < similarity:
                max_similarity = similarity
            max_similarity = similarity if max_similarity < similarity else max_similarity
        max_similarity = max_similarity if max_similarity > 0 else 0

        enrichment_score = EnrichmentContentScore.objects.filter(enrichment_id=enrichment.id).filter(term_id=term.id)
        if enrichment_score.exists():
            enrichment_score.update(score=max_similarity)
        else:
            scoring = EnrichmentContentScore(
                enrichment_id=enrichment.id,
                term_id=term.id,
                score=max_similarity
            )
            scoring.save()

    return