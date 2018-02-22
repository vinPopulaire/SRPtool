from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..models import Video

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

    return Response({"message": "Imported %d videos" %len(items)})

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
